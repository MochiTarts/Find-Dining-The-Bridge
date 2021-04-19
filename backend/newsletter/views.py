from django import forms
from django.db import transaction
from django.utils import timezone
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from newsletter.models import NLUser, NLAudit
from newsletter.serializer import NLUserInsertSerializer
from utils.model_util import model_to_json
from login_audit.models import get_client_ip_address

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from dateutil.relativedelta import relativedelta

import ast
import json
import jsonschema
from jsonschema import validate
import datetime
from datetime import date
from collections import namedtuple


USER_PICTURE = 'https://storage.googleapis.com/default-assets/user.png'

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

    @swagger_auto_schema(operation_id="POST /newsletter/signup")
    def post(self, request):
        """ insert a newsletter user into the db provided all the user fields """
        try:
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
        except jsonschema.ValidationError as e:
            try:
                message = e.schema['error_msg']
            except Exception:
                message = e.message
            finally:
                return JsonResponse({'message': message}, status=500)
        except json.decoder.JSONDecodeError as e:
            # Occurs when json request body is improperly formatted
            return JsonResponse({'message': e.message}, status=500)
        except ValueError as e:
            # Occurs when attempting to insert an object of the same email (since emails are unique)
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            # If any other exception occurs during insertion, remove the saved database objects (if any)
            NLUser.objects.filter(pk=body['email']).delete()
            message = 'Something went wrong'
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'Something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)


class NLUserDataView(APIView):
    """ Newsletter User Data View """

    @swagger_auto_schema(operation_id="POST /newsletter/user")
    def post(self, request):
        """ get user data associated with the user email """
        try:
            req_email = request.data.get('email')
            user = NLUser.objects.get(pk=req_email)
            return JsonResponse(model_to_dict(user))
        except ObjectDoesNotExist as e:
            if req_email is None:
                return JsonResponse({'message': "email cannot be Nonetype"}, status=404)
            return JsonResponse({'message': "The newsletter user profile with email: "+req_email+" does not exist."}, status=404)
