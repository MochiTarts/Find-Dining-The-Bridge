from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

#from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import json
from sduser.backends import jwt_decode
User = get_user_model()


class AdminPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email_admin.html'


class deactivateView(APIView):
    """ Deactivate user """
    #authentication_classes = [JWTAuthentication]

    def post(self, request):

        refresh_token = request.COOKIES.get('refresh_token')
        user_id = request.data.get('id')
        current_user = request.user

        if not current_user or current_user.id is not user_id:
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

            body = json.loads(request.body)
            user = User.objects.get(id=request.user.id)
            for field in body:
                setattr(user, field, body[field])
            user.save()
            return JsonResponse(model_to_dict(user))
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