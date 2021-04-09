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
from utils.permissions import ROPermission

from .models import RestaurantOwner
from restaurant.models import PendingRestaurant

from bson import ObjectId
import json

restaurant_owner_signup_schema = {
    "properties": {
        "restaurant_id": {"type": "string"},
        "last_updated": {"type": "string", "format": "date"},
        "consent_status": {"type": "string"},
        "subscribed_at": {"type": "string", "format": "date"},
        "unsubscribed_at": {"type": "string", "format": "date"},
        "expired_at": {"type": "string", "format": "date"},
    },
    "required": ["restaurant_id"],
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


class SignUp(APIView):
    """ Restaurant Owner signup view """
    permission_classes = [ROPermission]
    #permission_classes = (AllowAny,)

    def post(self, request):
        """ Inserts a new restaurant profile record into the database and attaches user_id to restaurant """
        user = request.user
        if not user:
            raise PermissionDenied(message="Failed to obtain user", code="fail_obtain_user")
        
        user_id = user.id
        validate(instance=request.data, schema=restaurant_owner_signup_schema)
        body = request.data
        RestaurantOwner.field_validate(body)
        
        body['user_id'] = user_id
        profile = RestaurantOwner.signup(body)
        return JsonResponse(model_to_json(profile))


class RestaurantOwnerView(APIView):
    """ Restaurant Owner view """
    permission_classes = [ROPermission]
    #permission_classes = (AllowAny,)

    def get(self, request):
        """ Retrieves a restaurant owner profile """
        user = request.user
        if not user:
            raise PermissionDenied(message="Failed to obtain user", code="fail_obtain_user")

        user_id = user.id
        restaurant_owner = RestaurantOwner.get_by_user_id(user_id=user_id)
        return JsonResponse(model_to_json(restaurant_owner))

    def put(self, request):
        """ Updates a restaurant owner profile """
        user = request.user
        if not user:
            raise PermissionDenied(message="Failed to obtain user", code="fail_obtain_user")

        user_id = user.id
        validate(instance=request.data, schema=restaurant_owner_edit_schema)
        body = request.data
        RestaurantOwner.field_validate(body)
        profile = RestaurantOwner.edit_profile(user_id, body)
        return JsonResponse(model_to_json(profile))