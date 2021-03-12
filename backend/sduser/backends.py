#from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django import forms

from .validators import validate_signup_user
from .forms import SDUserCreateForm
from .tokens import sduser_activation_token_generator

from smtplib import SMTPException

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

import json
import jwt


UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    authentication backend that authenticate user with username (or email) and password
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return UserModel.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


def signup(request):
    """
    validate registration form and create a disabled SDUser from the form (and sends verifiication email)
    """
    if request.method == 'POST':
        user = json.loads(request.body)
        invalid = validate_signup_user(user)
        username = user['username']
        email = user['email']
        password = user['password']

        if (len(invalid) == 0):
            try:
                if UserModel.objects.filter(username=username).exists():
                    return JsonResponse({'message': 'username already exists'}, status=400)
                elif UserModel.objects.filter(email=email).exists():
                    return JsonResponse({'message': 'email already exists'}, status=400)
                else:
                    return create_disable_user_and_send_verification_email(user, password, request)
            except Exception:
                return JsonResponse({'message': 'unable to create user'}, status=400)

        return JsonResponse({'invalid': invalid, 'message': 'Please make sure all fields are valid!'}, status=400)
    else:
        return JsonResponse({'Error': 'invalid request'}, status=404)


def create_disable_user_and_send_verification_email(user, password, request):
    """
    creates a disabled SDUser and send email verification

    returns a response indicating whether the operation is successful
    """
    form = SDUserCreateForm(data=user)

    if form.is_valid():
        user = UserModel.objects.create_user(
            username=user['username'], email=user['email'], password=user['password'], role=user['role'])
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        subject = 'Verify Your Email for Find Dining'
        message = render_to_string('verify_email/verification.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': sduser_activation_token_generator.make_token(user),
        })

        try:
            send_mail(subject, strip_tags(message), from_email='noreply<noreply@gmail.com>',
                      recipient_list=[user.email], html_message=message)
            # send a signal to frontend to ask them to verify email before log in
            return JsonResponse({'message': 'verification email has been sent. Please activate your account before sign in.'})
        except (BadHeaderError, SMTPException):
            user.delete()
            return JsonResponse({'message': 'there is some problem in the process of sending verification email. Please retry later or contact find dining support.'}, status=503)

    # this should never happen
    else:
        return JsonResponse({'message': 'invalid form'}, status=400)


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and not user.is_blocked and sduser_activation_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(
            request,
            template_name='verify_email/success.html',
            context={
                'msg': 'Thank you for confirming your email with Find Dining. Your account has been activated. Please click the button below to login.',
                'status': 'Verification Successful!',
                'link': reverse('login')
            }
        )
    else:
        return render(
            request,
            template_name='verify_email/failure.html',
            context={
                'msg': 'Activation link has been used or is invalid!',
                'status': 'Verification Failed!',
            }
        )


class SDUserCookieTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Token Obtain Pair Serializer
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom claims
        token['role'] = user.role
        token['username'] = user.username
        token['email'] = user.email

        return token


class SDUserCookieTokenObtainPairView(TokenObtainPairView):
    """
    Token Obtain Pair View with refresh token stored in the cookie
    """

    def finalize_response(self, request, response, *args, **kwargs):

        if response.data.get('refresh'):
            # 1 day
            cookie_max_age = 3600 * 24
            refresh_token = response.data['refresh']
            # note: setting path='/api/auth/refresh/' won't work
            response.set_cookie('refresh_token', refresh_token,
                                max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
            # decode token to get user info
            payload = jwt_decode(response.data['access'])
            # try:
            # store the refresh token inside user object
            user = UserModel.objects.get(id=payload['user_id'])
            user.refreshToken = refresh_token
            user.save()
        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = SDUserCookieTokenObtainPairSerializer


def jwt_decode(token):
    """
    decode a JWT issued from backend (our own auth)
    """
    try:
        return jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        return False  # Invalid token
    except jwt.ExpiredSignatureError:
        return False  # Token has expired
    except jwt.InvalidIssuerError:
        return False  # Token is not issued by Google
    except jwt.InvalidAudienceError:
        return False  # Token is not valid for this endpoint


class SDUserCookieTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Token Refresh Serializer
    """
    refresh = None

    def validate(self, attrs):
        """
        validate refresh token against db and its integrity
        """

        user_id = self.context['request'].data.get('user_id')
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')

        checkUserRefreshToken(user_id, attrs['refresh'])

        if attrs['refresh']:

            return super().validate(attrs)
        else:
            raise InvalidToken(
                'No valid token found in cookie \'refresh_token\'')


def checkUserRefreshToken(user_id, refresh_token):
    """
    check refresh token against the one stored in the db
    """
    if user_id is None:
        return InvalidToken('No user found who would have possessed this token')

    user = UserModel.objects.get(id=user_id)
    # validate the token against the one stored in the db (user object)
    if not refresh_token or refresh_token != user.refreshToken:
        raise InvalidToken(
            'Token mismatch: the token stored in cookie does not match the token in database')


class SDUserCookieTokenRefreshView(TokenRefreshView):
    """
    Token Refresh View
    """

    def finalize_response(self, request, response, *args, **kwargs):

        if response.data.get('refresh'):

            # 1 day
            cookie_max_age = 3600 * 24
            new_refresh_token = response.data['refresh']

            # try:
            user_id = request.data.get('user_id')

            # prevent anonymous user or disabled user to obtain new access and refresh token
            if user_id is None:
                return JsonResponse({'message': 'No user found', 'code': 'no_user_found'}, status=400)
            user = UserModel.objects.get(id=user_id)
            print(user)

            if user.is_blocked:
                return JsonResponse({'message': 'User has been blocked', 'code': 'user_blocked'}, status=401)

            if not user.is_active:
                return JsonResponse({'message': 'User has been disabled', 'code': 'user_disabled'}, status=401)

            response.set_cookie('refresh_token', new_refresh_token,
                                max_age=cookie_max_age, httponly=True)
            del response.data['refresh']

            # store the refresh token inside user object
            user.refreshToken = new_refresh_token
            user.save()

        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = SDUserCookieTokenRefreshSerializer
