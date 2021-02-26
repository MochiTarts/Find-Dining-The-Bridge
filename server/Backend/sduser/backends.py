from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from rest_framework_jwt import utils
from django.http import HttpResponse, JsonResponse
from .validators import validate_signup_user
from .forms import SDUserCreateForm
from verify_email.email_handler import send_verification_email
from django.contrib.auth.forms import UserCreationForm
from django import forms
import json

UserModel = get_user_model()


class EmailBackend(ModelBackend):
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


# add role to the payload
def jwt_payload_handler(user):
    payload = utils.jwt_payload_handler(user)
    payload['role'] = user.role
    payload['email_verified'] = user.email_verified

    return payload


def signup(request):
    if request.method == 'POST':
        user = json.loads(request.body)
        invalid = validate_signup_user(user)
        username = user['username']
        email = user['email']
        if (len(invalid)==0):
            try:
                if UserModel.objects.filter(username=username).exists():
                    return JsonResponse({'message': 'username already exists'}, status=400)
                elif UserModel.objects.filter(email=email).exists():
                    return JsonResponse({'message': 'email already exists'}, status=400)
                else:
                    form = SDUserCreateForm(data=user)
                    if form.is_valid():
                        # note that send_verification_email would create an inactive user so we no longer need to create user object ourselves
                        # user = UserModel.objects.create_user(username=username, email=email, password=user['password'], role=user['role'])
                        inactive_user = send_verification_email(request, form)
                        return HttpResponse()
                    else:
                        return JsonResponse({'message': 'unable to create user'}, status=400)
            except Exception:
                return JsonResponse({'message': 'unable to create user'}, status=400)
            
        return JsonResponse({'invalid': invalid, 'message': 'Please make sure all fields are valid!'}, status=400)
    else:
        return JsonResponse({'Error': 'Invalid Request 2'}, status=404)