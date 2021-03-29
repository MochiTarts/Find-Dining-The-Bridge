from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import BadHeaderError
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

#from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from utils.math import get_nearby_restaurants
from sduser.utils import send_email_password_reset

import json
import ast

User = get_user_model()


class AdminPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email_admin.html'


class SDUserPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email_admin.html'


class deactivateView(APIView):
    """ Deactivate user """
    #authentication_classes = [JWTAuthentication]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        user_id = request.data.get('id')
        current_user = request.user

        if not current_user:
            return JsonResponse({'message': 'fail to obtain user', 'code': 'deactivation_fail'}, status=405)

        if current_user.id is not user_id:
            return JsonResponse({'message': 'deactivation failed: user mismatch!', 'code': 'deactivation_fail'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            if refresh_token == user.refresh_token:
                user.is_active = False
                user.save()
                return JsonResponse(model_to_dict(user))
            else:
                return JsonResponse({'message': 'deactivation failed: token mismatch', 'code': 'deactivation_fail'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'deactivation failed: User not found', 'code': 'deactivation_fail'}, status=400)


class editView(APIView):
    """ Edit user """

    def put(self, request):
        try:
            body = request.data
            user = request.user
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)

            for field in body:
                setattr(user, field, body[field])
            user.save()
            return JsonResponse(model_to_dict(user))
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            message = ''
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', "something went wrong")
            finally:
                return JsonResponse({'message': message}, status=500)


class NearbyRestaurantsView(APIView):
    """ Get nearby restaurants from a restaurant owner """
    #permission_classes = (AllowAny,)

    def get(self, request):
        """ Retrieves the 5 (or less) nearest restaurants from an sduser """
        user = user.request
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user", code="fail_obtain_user")

        user_id = user.id
        role = user.role
        nearest = get_nearby_restaurants(user_id, role)
        return JsonResponse(nearest, safe=False)

class SDUserPasswordResetView(APIView):
    """ password reset view """
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        associated_users = User.objects.filter(Q(email=email))
        
        if not associated_users.exists():
            raise ObjectDoesNotExist("No user associated with email: " + email)
        if associated_users.count() > 1:
            raise MultipleObjectsReturned("There are more than one User associated with email: " + email)
        user = associated_users.first()
        try:
            send_email_password_reset(user=user, request=request)
        except BadHeaderError:
            return JsonResponse({'message':'Invalid header found.'}, status=400)

        return JsonResponse({'message': 'Password reset email has been sent'})

