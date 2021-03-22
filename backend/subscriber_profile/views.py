import json

from django.shortcuts import render
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import SubscriberProfile


class Signup(APIView):
    def put(self, request):
        try:
            body = json.loads(request.body)
            invalid = SubscriberProfile.field_validate(body)
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
    def get(self, request):
        try:
            body = json.loads(request.body)
            invalid = SubscriberProfile.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            profile = SubscriberProfile.objects.get(id=body['id'])
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
