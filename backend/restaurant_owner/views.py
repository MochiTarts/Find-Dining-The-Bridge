from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from utils.model_util import model_to_json, save_and_clean, edit_model, update_model_geo, models_to_json
from .models import RestaurantOwner
from restaurant.models import PendingRestaurant

from bson import ObjectId
import ast
import json

restaurant_owner_signup_schema = {
    "properties": {
        "user_id": {"type": "number"},
        "restaurant_id": {"type": "string"},
        "last_updated": {"type": "string", "format": "date"},
        "consent_status": {"type": "string"},
        "subscribed_at": {"type": "string", "format": "date"},
        "unsubscribed_at": {"type": "string", "format": "date"},
        "expired_at": {"type": "string", "format": "date"},
    },
    "required": ["user_id"],
    "additionalProperties": False
}

restaurant_owner_edit_schema = {
    "properties": {
        "restaurant_id": {"type": "string"},
        "last_updated": {"type": "string", "format": "date"},
        "consent_status": {"type": "string"},
        "subscribed_at": {"type": "string", "format": "date"},
        "unsubscribed_at": {"type": "string", "format": "date"},
        "expired_at": {"type": "string", "format": "date"},
    },
    "additionalProperties": False
}

restaurant_owner_editable = [
   "restaurant_id", "last_updated", "consent_status", "subscribed_at", "unsubscribed_at", "expired_at"
]


class SignUp(APIView):
    """ Restaurant Owner signup view """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """ Inserts a new restaurant profile record into the database and attaches user_id to restaurant """
        try:
            validate(instance=json.loads(request.body), schema=restaurant_owner_signup_schema)
            body = request.data
            invalid = RestaurantOwner.field_validate(body)
            restaurant_filter = PendingRestaurant.objects.filter(_id=body['restaurant_id'])
            if invalid:
                return JsonResponse(invalid, status=400)
            if RestaurantOwner.objects.filter(user_id=body['user_id']).exists():
                return JsonResponse({"message": "Profile with this user_id already exists"}, status=400)
            if not restaurant_filter.exists():
                return JsonResponse({"message": "This restaurant_id does not exist"}, status=400)
            
            profile = RestaurantOwner.signup(body)
            restaurant = restaurant_filter.first()
            restaurant.owner_user_id = body['user_id']
            save_and_clean(restaurant)
            return JsonResponse(model_to_json(profile))
        except ValidationError as e:
            return JsonResponse({"message": e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({"message": e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            message = 'something went wrong'
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)


class RestaurantOwnerView(APIView):
    """ Restaurant Owner view """
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        """ Retrieves a restaurant owner profile """
        try:
            ro_filter = RestaurantOwner.objects.filter(user_id=user_id)
            if ro_filter.exists():
                return JsonResponse(model_to_json(ro_filter.first()))
            else:
                return JsonResponse({"message": "This restaurant owner profile does not exist"}, status=404)
        except Exception as e:
            message = ''
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', "something went wrong")
            finally:
                return JsonResponse({'message': message}, status=500)

    def put(self, request, user_id):
        """ Updates a restaurant owner profile """
        try:
            validate(instance=json.loads(request.body), schema=restaurant_owner_edit_schema)
            body = request.data
            invalid = RestaurantOwner.field_validate(body)
            profile = {}
            ro_filter = RestaurantOwner.objects.filter(user_id=user_id)
            
            if not ro_filter.exists():
                return JsonResponse({"message": "This restaurant owner profile does not exist"}, status=404)
            else:
                profile = ro_filter.first()
            if not PendingRestaurant.objects.filter(_id=body['restaurant_id']).exists():
                return JsonResponse({"message": "This restaurant_id does not exist"}, status=400)

            edit_model(profile, body, restaurant_owner_editable)
            profile = save_and_clean(profile)
            return JsonResponse(model_to_json(profile))
        except ValidationError as e:
            return JsonResponse({"message": e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({"message": e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            message = 'something went wrong'
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)