from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.conf import settings

from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from sduser.backends import SDUserCookieTokenObtainPairSerializer, create_disable_user_and_send_verification_email
from sduser.forms import SDUserCreateForm

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

import requests

User = get_user_model()


class GoogleView(APIView):
    """
    auth view for authenticating log in request with Google
    """

    # this is to allow handling log in request (obviously they are not logged in when making the request)
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        FLOW 1 (for new signup)
        creates a disabled SDUser and associate it with the google account,
        if for any reason the google account has unverified email,
        it will send a verification email to that address

        returns messages indicating the above for frontend to handle

        FLOW 2 (for verified user)
        updates the SDUser associated with the google account
        and authenticate this user

        returns access token in response body with refresh token set in the httpOnly cookie
        """

        payload = {'access_token': request.data.get("authToken")}
        # verify the token and use it to get user info
        r = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)
        print(data)

        if 'error' in data:
            content = {
                'message': 'wrong google token / this google token is already expired.'}
            return Response(content)
        
        auth_id = data['id']
        # this should be the same as the one obtained from google idToken
        email = data['email']
        role = request.data.get('role')

        try:
            googleJWT = id_token.verify_oauth2_token(request.data.get(
                'idToken'), google_requests.Request(), settings.GOOGLE_OAUTH2_CLIENT_ID)
            print('user info from google idToken:')
            print(googleJWT)
            # this is definitive as it is not modifiable
            email = googleJWT['email']
            # get user by auth Id (3rd party id) Or email
            user = User.objects.get(
                Q(auth_id__iexact=auth_id) | Q(email__iexact=email))
            if user.email is not email:
                user.email = email
                user.save()
        # if verify_oauth2_token failed
        except ValueError:
            return JsonResponse({'message': 'idToken is invalid'}, status=400)
        # if user not in db, create one with random password
        except User.DoesNotExist:
            user = create_default_user_for_3rd_party(email, auth_id, role)

            # if email is verified with 3rd party we can simply save the user with an 3rd party id
            if googleJWT['email_verified']:
                user.auth_id = auth_id
                user.save()
            # otherwise we create a disabled user and send an email for verification
            else:
                return create_disable_user_and_send_verification_email(user, password, request)

        response = construct_response_for_3rd_party_auth(user)

        return response


class FacebookView(APIView):
    """
    auth view for authenticating log in request with Facebook
    """

    # this is to allow handling log in request (obviously they are not logged in when making the request)
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        FLOW 1 (for new signup)
        creates a disabled SDUser, associate it with the facebook account
        (facebook requires email to be verified so there is no need to handle it)

        returns messages indicating the above for frontend to handle

        FLOW 2 (for verified user)
        updates the SDUser associated with the facebook account
        and authenticate this user

        returns access token in response body with refresh token set in the httpOnly cookie
        """

        payload = {
            'access_token': request.data.get("authToken"),
            'fields': ','.join(['id', 'birthday', 'email', 'first_name', 'last_name', 'name'])
        }
        # use auth token and user id to get user info (get above fields)
        r = requests.get('https://graph.facebook.com/v10.0/' +
                         request.data.get('id'), params=payload)
        data = json.loads(r.text)

        print('user profile fields from facebook:')
        print(data)

        if 'error' in data:
            content = {'message': 'invalid facebook token or user id'}
            return Response(content)

        auth_id = data['id']
        email = data['email']
        role = request.data.get('role')

        try:
            # get user by auth Id (3rd party id) Or email
            user = User.objects.get(
                Q(auth_id__iexact=auth_id) | Q(email__iexact=email))
            # update user email in case they updated it in 3rd party service
            # we can also ask it before update (future enhancements)
            if user.email is not email:
                user.email = email
                user.save()

        # if user not in db, create one with random password
        except User.DoesNotExist:
            user = create_default_user_for_3rd_party(email, auth_id, role)

        response = construct_response_for_3rd_party_auth(user)

        return response


def construct_response_for_3rd_party_auth(user):
    """
    construct authentication response and update user with refresh token

    user -- a SDUser

    returns a response containing access token (and refresh token in httpOnly cookie)
    """
    # generate token without username & password
    # need to use customized one to have all the information we need
    #token = RefreshToken.for_user(user)
    token = SDUserCookieTokenObtainPairSerializer.get_token(user)

    response = {}
    #response['username'] = user.username
    response['access_token'] = str(token.access_token)
    #response['refresh_token'] = str(token)
    cookie_max_age = 3600 * 24
    # print(dir(token))
    refresh_token = str(token)
    user.refresh_token = refresh_token
    user.save()
    res = Response(response)
    res.set_cookie('refresh_token', refresh_token,
                   max_age=cookie_max_age, httponly=True)

    return res


def create_default_user_for_3rd_party(email, auth_id, role):
    """
    create a default SDUser for 3rd party

    email -- email for user
    auth_id -- 3rd party user id (should be unique for the 3rd party)

    returns the created user
    """
    user = User()
    user.username = email
    # provide a random default password
    password = make_password(BaseUserManager().make_random_password())
    user.password = password
    user.email = email
    user.role = role

    # note that facebook users have their email verified so we do not need to check it
    user.auth_id = auth_id
    user.save()
    return user
