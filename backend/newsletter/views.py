from django import forms
from django.db import transaction
from django.utils import timezone
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from newsletter.models import NLUser, NLAudit
from newsletter.serializer import NLUserInsertSerializer
from newsletter import swagger
from utils.model_util import model_to_json
from login_audit.models import get_client_ip_address

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from dateutil.relativedelta import relativedelta

import jsonschema
from jsonschema import validate
import datetime
from datetime import date

# jsonschema validation scheme
newsletter_signup_schema = {
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 1,
            "error_msg": "First name cannot be empty."
        },
        "last_name": {
            "type": "string",
            "minLength": 1,
            "error_msg": "Last name cannot be empty."
        },
        "email": {
            "type": "string",
            "minLength": 1,
            "error_msg": "Email cannot be empty."
        },
        "consent_status": {
            "type": "string",
            "minLength": 1,
            "error_msg": "Consent status cannot be empty."
        }
    },
    "required": ["first_name", "last_name", "email", "consent_status"]
}


class NLUserSignupView(APIView):
    """ Newsletter User View """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=swagger.NLUserInsert,
        responses=swagger.nluser_signup_post_response, operation_id="POST /newsletter/signup")
    def post(self, request):
        """ insert a newsletter user into the db provided all the user fields """
        validate(instance=request.data,
                    schema=newsletter_signup_schema)
        body = request.data

        ip = get_client_ip_address(request)
        block = NLAudit.update_audit(ip)
        if block:
            msg = "You have submitted too many signups and have been temporarily blocked. Please do not spam our system!"
            return JsonResponse({'message': msg}, status=500)
        invalid = NLUser.field_validate(body)
        if invalid:
            return JsonResponse(invalid, status=400)
        user = NLUser.signup(first_name=body['first_name'], last_name=body['last_name'], email=body['email'],
                                consent_status=body['consent_status'], expired_at=date.today() + relativedelta(months=+6))
        return JsonResponse(model_to_dict(user))


class NLUserDataView(APIView):
    """ Newsletter User Data View """

    @swagger_auto_schema(responses=swagger.nluser_profile_get_response,
        operation_id="GET /newsletter/user")
    def get(self, request):
        """ get user data associated with the user email """
        req_email = request.data.get('email')
        user = NLUser.objects.get(pk=req_email)
        return JsonResponse(model_to_dict(user))
