#from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Q
from django import forms

from sduser.validators import validate_signup_user
from sduser.forms import SDUserCreateForm

from smtplib import SMTPException

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from login_audit.models import AuditEntry, get_client_http_accept, get_client_path_info, get_client_user_agent
from sduser.utils import send_email_verification, verify_email

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
            return UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()
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
                if UserModel.objects.filter(username__iexact=username).exists():
                    return JsonResponse({'message': 'username already exists'}, status=400)
                elif UserModel.objects.filter(email__iexact=email).exists():
                    return JsonResponse({'message': 'email already exists'}, status=400)
                else:
                    return create_disable_user_and_send_verification_email(user, password, request)
            except Exception as e:
                print(str(e))
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

        try:
            send_email_verification(user, request)
            # send a signal to frontend to ask them to verify email before log in
            return JsonResponse({'message': "verification email has been sent. Please activate your account before sign in. If you don't receive an email, please check your spam folder or contact us from your email address and we can verify it for you."})
        except (BadHeaderError, SMTPException):
            user.delete()
            return JsonResponse({'message': 'there is some problem in the process of sending verification email. Please retry later or contact find dining support.'}, status=503)

    # this should never happen
    else:
        return JsonResponse({'message': 'invalid form'}, status=400)


def check_user_status(user):
    """
    check on user is_disabled and is_blocked status and
    raise appropriate error with detail messages for login to display
    """
    if user.is_blocked:
        raise AuthenticationFailed(
            'This user has been blocked. If you think this is a mistake, please contact find dining team to resolve it',
            'user_blocked',
        )
    elif not user.is_active:
        raise AuthenticationFailed(
            'This user is disabled.',
            'user_disabled',
        )


class SDUserCookieTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Token Obtain Pair Serializer
    """

    def validate(self, attrs):
        """
        simple check on user status before authenticate
        """
        username = attrs['username']

        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username))
            check_user_status(user)
        except UserModel.DoesNotExist:
            raise AuthenticationFailed(
                'User does not exist',
                'user_not_found',
            )
        except MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(
                email__iexact=username)).order_by('id').first()
            check_user_status(user)

        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom claims
        token['role'] = user.role
        token['username'] = user.username
        token['email'] = user.email
        token['profile_id'] = user.profile_id

        #token['id'] = user.id

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
            user.refresh_token = refresh_token
            user.save()

            # this is how we can trigger the logged in signal but we wouldn't be able to get client ip
            #user_logged_in.send(sender=user.__class__, request=request, user=user)

            # so we need to create the log entry manually
            AuditEntry.objects.create(
                action='logged in',
                username=user.username,
                attempt_time=timezone.now(),
                user_agent=get_client_user_agent(request),
                ip_address=request.data.get('ip'),
                path_info=get_client_path_info(request),
                http_accept=get_client_http_accept(request)
            )

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
    if not refresh_token or refresh_token != user.refresh_token:
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

            access_token = response.data.get('access')
            if access_token:
                old_user = jwt_decode(access_token)

                if old_user['profile_id'] is None:
                    del response.data['access']
                    # need to obtain it manually because we need to update the profile id (by forcing a read from the db)
                    new_token = SDUserCookieTokenObtainPairSerializer.get_token(user)
                    response.data['access'] = str(new_token.access_token)
                    # also update the refresh token
                    new_refresh_token = str(new_token)

            if user.is_blocked:
                return JsonResponse({'message': 'User has been blocked', 'code': 'user_blocked'}, status=401)

            if not user.is_active:
                return JsonResponse({'message': 'User has been disabled', 'code': 'user_disabled'}, status=401)

            response.set_cookie('refresh_token', new_refresh_token,
                                max_age=cookie_max_age, httponly=True)
            del response.data['refresh']

            # store the refresh token inside user object
            user.refresh_token = new_refresh_token
            user.save()

        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = SDUserCookieTokenRefreshSerializer
