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



User = get_user_model()

class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class GoogleView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            # provider random default password
            password = make_password(BaseUserManager().make_random_password())
            user.password = password
            user.email = data['email']
            #user.save()

            form = SDUserCreateForm(data=user)
            if form.is_valid():
                # note that send_verification_email would create an inactive user so we no longer need to create user object ourselves
                # user = UserModel.objects.create_user(username=username, email=email, password=user['password'], role=user['role'])
                inactive_user = send_verification_email(request, form)
                # need to set password manually to have it properly hashed
                inactive_user.set_password(password)
                inactive_user.save()

                return HttpResponse()
            else:
                return JsonResponse({'message': 'invalid form'}, status=400)

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        #response['refresh_token'] = str(token)
        cookie_max_age = 3600 * 24
        #print(dir(token))
        refresh_token = str(token)
        res = Response(response)
        res.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True )
        
        return Response(response)
