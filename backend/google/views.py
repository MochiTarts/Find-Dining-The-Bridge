from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from verify_email.email_handler import send_verification_email
from sduser.forms import SDUserCreateForm
from sduser.backends import jwt_decode_no_sig
from django.db.models import Q

User = get_user_model()

class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class GoogleView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        
        payload = {'access_token': request.data.get("authToken")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)
        print(data)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        googleJWT = jwt_decode_no_sig(request.data.get('idToken'))

        auth_id = data['id']
        email = googleJWT['email']
        # create user if not exist
        try:
            #user = User.objects.get(email=data['email'])
            # get user by auth Id (3rd party id) Or email
            user = User.objects.get(
                Q(authId__iexact=data['id']) | Q(email__iexact=email))
            if user.email is not email:
                user.email = email
                user.save()

        except User.DoesNotExist:
            user = User()
            user.username = email
            # provider random default password
            password = make_password(BaseUserManager().make_random_password())
            user.password = password
            user.email = email
            #user.role = data['role']
            user.role = 'BU'
            
            # if email is verified with 3rd party
            if googleJWT['email_verified']:
                user.authId = auth_id
                user.save()
            else:
                form = SDUserCreateForm(data=user)
                if form.is_valid():
                    # note that send_verification_email would create an inactive user so we no longer need to create user object ourselves
                    # user = User.objects.create_user(username=username, email=email, password=user['password'], role=user['role'])
                    inactive_user = send_verification_email(request, form)
                    # need to set password manually to have it properly hashed
                    inactive_user.set_password(password)
                    inactive_user.save()
                    #return HttpResponse()
                else:
                    return JsonResponse({'message': 'invalid form'}, status=400)

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        #response['username'] = user.username
        response['access_token'] = str(token.access_token)
        #response['refresh_token'] = str(token)
        cookie_max_age = 3600 * 24
        #print(dir(token))
        refresh_token = str(token)
        user.refreshToken = refresh_token
        user.save()
        res = Response(response)
        res.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True )
        
        return Response(response)
