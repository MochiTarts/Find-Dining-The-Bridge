import json

from django.shortcuts import render
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import SubscriberProfile


class Signup(APIView):
    #permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            body = json.loads(request.body)
            invalid = SubscriberProfile.field_validate(body)
            if SubscriberProfile.objects.filter(pk=body['user_id']).exists():
                if not invalid:
                    invalid = {"Invalid": "Profile with this user_id already exists"}
                else:
                    invalid['Invalid'].append("Profile with this user_id already exists")
            print(invalid)
            if invalid:
                return JsonResponse(invalid, status=400)
            profile = SubscriberProfile.signup(body)
            return JsonResponse(model_to_dict(profile))
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            body = json.loads(request.body)
            message = ''
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', "something went wrong")
            finally:
                return JsonResponse({'message': message}, status=500)


class SubscriberProfileView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            profile = SubscriberProfile.objects.get(pk=user_id)
            return JsonResponse(model_to_dict(profile))
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            body = json.loads(request.body)
            message = ''
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', "something went wrong")
            finally:
                return JsonResponse({'message': message}, status=500)

    def put(self, request):
        try:
            body = json.loads(request.body)
            invalid = SubscriberProfile.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            profile = SubscriberProfile.edit(body)
            return JsonResponse(model_to_dict(profile))
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            body = json.loads(request.body)
            message = ''
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', "something went wrong")
            finally:
                return JsonResponse({'message': message}, status=500)
