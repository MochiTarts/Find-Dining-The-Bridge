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


class Signup(APIView):

    def post(self, request):
        body = request.data
        user = request.user
        if not user:
            raise PermissionDenied(message="Failed to obtain user", code="fail_obtain_user")
        body['user_id'] = user.id
        SubscriberProfile.field_validate(body)
        if SubscriberProfile.objects.filter(user_id=body['user_id']).exists():
            raise IntegrityError('Cannot insert subscriber profile, an object with this user id already exists')
        profile = SubscriberProfile.signup(body)
        return JsonResponse(model_to_json(profile))


class SubscriberProfileView(APIView):

    def get(self, request):
        user = request.user
        if not user:
            raise PermissionDenied(message="Failed to obtain user", code="fail_obtain_user")
        profile = SubscriberProfile.objects.get(user_id=user.id)
        if not profile:
            raise ObjectDoesNotExist('No subscriber profile found with owner user id of this: ' + user_id)
        return JsonResponse(model_to_dict(profile))

    def put(self, request):
        body = request.data
        user = request.user
        if not user:
            raise PermissionDenied(message="Failed to obtain user", code="fail_obtain_user")
        body['user_id'] = user.id
        SubscriberProfile.field_validate(body)
        profile = SubscriberProfile.edit(body)
        return JsonResponse(model_to_json(profile))