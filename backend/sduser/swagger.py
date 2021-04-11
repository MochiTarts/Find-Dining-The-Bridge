from django.contrib.auth import get_user_model
from rest_framework import serializers
from .enum import Roles

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

User = get_user_model()

user_nearby_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": [
                {
                    'restaurant': '605b55d192c9e40e98c1877a',
                    'distance': 0.09441842712978067
                },
                {
                    'restaurant': '60633190ecd9bcd74ce3e50a',
                    'distance': 39.827594937396
                },
                {
                    'restaurant': '606c67d572a3c3069cf8621a',
                    'distance': 39.827594937396
                },
                {
                    'restaurant': '606c682572a3c3069cf8621b',
                    'distance': 39.827594937396
                },
                {
                    'restaurant': '606c683c72a3c3069cf8621c',
                    'distance': 39.827594937396
                }
            ]
        }
    )
}