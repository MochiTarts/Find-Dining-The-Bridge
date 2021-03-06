from django import forms
from django.db import transaction
from django.utils import timezone
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from newsletter.models import NLUser, NLAudit
from newsletter import schemas
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


class NLUserSignupView(APIView):
    """ Newsletter User View """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=swagger.NLUserInsert,
        responses=swagger.nluser_signup_post_response, operation_id="POST /newsletter/signup")
    def post(self, request):
        """ insert a newsletter user into the db provided all the user fields """
        validate(instance=request.data,
                    schema=schemas.newsletter_signup_schema)
        body = request.data

        ip = get_client_ip_address(request)
        block = NLAudit.update_audit(ip)
        if block:
            msg = "You have submitted too many signups and have been temporarily blocked. Please do not spam our system!"
            return JsonResponse(
                {'status': 500, 'code': 'too_many_signups', 'detail': msg}, status=500)
        NLUser.field_validate(body)
        user = NLUser.signup(
            first_name=body['first_name'],
            last_name=body['last_name'],
            email=body['email'],
            consent_status=body['consent_status'],
            expired_at=date.today() + relativedelta(days=+182))
        return JsonResponse(model_to_json(user))


class NLUserDataView(APIView):
    """ Newsletter User Data View """

    @swagger_auto_schema(responses=swagger.nluser_profile_get_response,
        operation_id="GET /newsletter/user")
    def get(self, request):
        """ get user data associated with the user email """
        req_email = request.data.get('email')
        user = NLUser.get(req_email)
        return JsonResponse(model_to_json(user))
