from django.shortcuts import render
from django.forms import model_to_dict
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from subscriber_profile.models import SubscriberProfile
from restaurant.models import Restaurant

from utils.model_util import model_to_json
from utils.common import get_user
from utils.math import calculate_distance

import json
from operator import itemgetter
import ast


class Signup(APIView):

    def post(self, request):
        try:
            body = request.data
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            body['user_id'] = user['user_id']
            invalid = SubscriberProfile.field_validate(body)
            if SubscriberProfile.objects.filter(user_id=body['user_id']).exists():
                if not invalid:
                    invalid = {"Invalid": "Profile with this user_id already exists"}
                else:
                    invalid['Invalid'].append("Profile with this user_id already exists")
            if invalid:
                return JsonResponse(invalid, status=400)
            profile = SubscriberProfile.signup(body)
            return JsonResponse(model_to_json(profile))
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


class SubscriberProfileView(APIView):

    def get(self, request):
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)

            profile = SubscriberProfile.objects.get(user_id=user['user_id'])
            return JsonResponse(model_to_dict(profile))
        except SubscriberProfile.DoesNotExist as e:
            return JsonResponse({'message': "no profile found!", 'code': "no_profile_found"}, status=400)
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

    def put(self, request):
        try:
            body = request.data
            user = get_user(request)

            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            body['user_id'] = user['user_id']
            invalid = SubscriberProfile.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            profile = SubscriberProfile.edit(body)
            return JsonResponse(model_to_json(profile))
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


class ConsentStatusView(APIView):

    def put(self, request):
        try:
            body = request.data
            user = get_user(request)

            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            body['user_id'] = user['user_id']
            invalid = SubscriberProfile.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            profile = SubscriberProfile.edit(body)
            return JsonResponse(model_to_dict(profile))
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
    """ Get nearby restaurants from a subscriber """
    permission_classes = (AllowAny,)

    def get(self, request, user_id):
        """ Retrieves the 5 (or less) nearest restaurants from a subscriber provided the user_id """
        try:
            user = SubscriberProfile.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({"message": "The user with this user_id does not exist"}, status=400)
            user_location = ast.literal_eval(user.GEO_location)
            
            nearest = []
            restaurants = list(Restaurant.objects.all())
            for restaurant in restaurants:
                rest_location = ast.literal_eval(restaurant.GEO_location)
                distance = calculate_distance(user_location, rest_location)
                nearest.append({"restaurant": str(restaurant._id), "distance": distance})

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