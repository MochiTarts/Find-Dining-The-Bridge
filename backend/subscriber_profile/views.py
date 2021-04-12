from django.shortcuts import render
from django.forms import model_to_dict
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from subscriber_profile.models import SubscriberProfile

from utils.model_util import model_to_json

import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from subscriber_profile import swagger


class Signup(APIView):
    """ SubscriberProfile signup view """

    @swagger_auto_schema(request_body=swagger.SubscriberProfileInsert,
        responses=swagger.subscriber_profile_signup_post_response)
    def post(self, request):
        """ Inserts a new SubscriberProfile record into the database """
        body = request.data
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")
        body['user_id'] = user.id
        SubscriberProfile.field_validate(body)
        if SubscriberProfile.objects.filter(user_id=body['user_id']).exists():
            raise IntegrityError(
                'Cannot insert subscriber profile, an object with this user id already exists')
        profile = SubscriberProfile.signup(body)
        return JsonResponse(model_to_json(profile))


class SubscriberProfileView(APIView):
    """ SubscriberProfile get and update view """

    @swagger_auto_schema(responses=swagger.subscriber_profile_profile_get_response)
    def get(self, request):
        """ Retrieves a SubscriberProfile record from the database """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")
        profile = SubscriberProfile.objects.get(user_id=user.id)
        if not profile:
            raise ObjectDoesNotExist(
                'No subscriber profile found with owner user id of this: ' + str(user_id))
        return JsonResponse(model_to_dict(profile))

    @swagger_auto_schema(request_body=swagger.SubscriberProfileUpdate,
        responses=swagger.subscriber_profile_profile_put_response)
    def put(self, request):
        """ Modifies a SubscriberProfile record in the database """
        body = request.data
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")
        body['user_id'] = user.id
        SubscriberProfile.field_validate(body)
        profile = SubscriberProfile.edit(body)
        return JsonResponse(model_to_json(profile))