from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Q
from django import forms

from .validators import validate_signup_user
from .forms import SDUserCreateForm

from verify_email.email_handler import send_verification_email

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
        if (len(invalid)==0):
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
        # note that send_verification_email would create an inactive user so we no longer need to create user object ourselves
        # user = User.objects.create_user(username=username, email=email, password=user['password'], role=user['role'])
        inactive_user = send_verification_email(request, form)
        # need to set password manually to have it properly hashed
        inactive_user.set_password(password)
        inactive_user.save()
        # send a signal to frontend to ask them to verify email before log in
        return JsonResponse({'message': 'A verification email has been sent. Please verify your email and sign in again.'})
    # this should never happen
    else:
        return JsonResponse({'message': 'invalid form'}, status=400)


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
            response.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
            # decode token to get user info
            payload = jwt_decode(response.data['access'])
            #try:
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
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

def checkUserRefreshToken(user_id, refresh_token):
    """
    check refresh token against the one stored in the db
    """
    if user_id is None:
        return InvalidToken('No user found who would have possessed this token')

    user = UserModel.objects.get(id=user_id)
    # validate the token against the one stored in the db (user object)
    if not refresh_token or refresh_token != user.refreshToken:
        raise InvalidToken('Token mismatch: the token stored in cookie does not match the token in database')
    


class SDUserCookieTokenRefreshView(TokenRefreshView):
    """
    Token Refresh View
    """
    def finalize_response(self, request, response, *args, **kwargs):

        if response.data.get('refresh'):

            # 1 day
            cookie_max_age = 3600 * 24
            new_refresh_token = response.data['refresh']

            #try:
            user_id = request.data.get('user_id')

            # prevent anonymous user or disabled user to obtain new access and refresh token 
            if user_id is None:
                return JsonResponse({'message':'No user found', 'code': 'no_user_found'},status=400)
            user = UserModel.objects.get(id=user_id)
            print(user)

            if not user.is_active:
                return JsonResponse({'message':'User has been disabled', 'code': 'user_disabled'},status=401)


            response.set_cookie('refresh_token', new_refresh_token, max_age=cookie_max_age, httponly=True )
            del response.data['refresh']

            # store the refresh token inside user object
            user.refreshToken = new_refresh_token
            user.save()

        return super().finalize_response(request, response, *args, **kwargs)
    
    serializer_class = SDUserCookieTokenRefreshSerializer