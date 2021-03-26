from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

#from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils.common import get_user
from utils.math import calculate_distance

from subscriber_profile.models import SubscriberProfile
from restaurant.models import PendingRestaurant, Restaurant

import json
from operator import itemgetter
import ast

User = get_user_model()


class AdminPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email_admin.html'


class deactivateView(APIView):
    """ Deactivate user """
    #authentication_classes = [JWTAuthentication]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        user_id = request.data.get('id')
        current_user = get_user(request)
        if not current_user:
            return JsonResponse({'message': 'fail to obtain user', 'code': 'deactivation_fail'}, status=405)

        if current_user['user_id'] is not user_id:
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
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user = User.objects.get(id=user['user_id'])
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
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']
            role = user['role']
            user = None

            if role == 'BU':
                user = SubscriberProfile.objects.filter(
                    user_id=user_id).first()
            else:
                user = PendingRestaurant.objects.filter(
                    owner_user_id=user_id).first()

            if not user:
                return JsonResponse({"message": "The user with this user_id does not exist"}, status=400)
            user_location = ast.literal_eval(user.GEO_location)

            nearest = []
            restaurants = list(Restaurant.objects.all())
            for restaurant in restaurants:
                if role == 'RO' and restaurant._id == user._id:
                    continue
                user_location = ast.literal_eval(restaurant.GEO_location)
                distance = calculate_distance(user_location, user_location)
                nearest.append(
                    {"restaurant": str(restaurant._id), "distance": distance})

            nearest = sorted(nearest, key=itemgetter("distance"))
            if (len(nearest) > 5):
                nearest = nearest[:5]
            return JsonResponse(nearest, safe=False)
        except Exception as e:
            message = ''
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', "something went wrong")
            finally:
                return JsonResponse({'message': message}, status=500)
