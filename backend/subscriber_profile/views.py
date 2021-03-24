import json

from django.shortcuts import render
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import SubscriberProfile
from utils.model_util import model_to_json


class Signup(APIView):

    def post(self, request):
        try:
            body = request.data
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
            #user_id = request.GET.get('user_id')
            user_id = request.user.id
            profile = SubscriberProfile.objects.get(user_id=user_id)
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
            body['user_id'] = request.user.id
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
            body['user_id'] = request.user.id
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