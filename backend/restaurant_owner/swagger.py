from .models import RestaurantOwner
from rest_framework import serializers
from .enum import ConsentStatus

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response


class RestaurantOwnerInsert(serializers.Serializer):
    restaurant_id = serializers.CharField(max_length=24)
    consent_status = serializers.ChoiceField(
        required=False, choices=ConsentStatus.choices())

    class Meta:
        ref_name = None


restaurant_owner_signup_post_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "consent_status": "IMPLIED",
                "expired_at": "2021-09-29T00:00:00.000+00:00",
                "id": 10,
                "last_updated": "2021-03-25T00:00:00.000+00:00",
                "restaurant_id": "605b55d192c9e40e98c1877a",
                "subscribed_at": None,
                "unsubscribed_at": None,
                "user_id": 107,
                "_id": "605cbe3ee8bf2b279ae052ee"
            }
        }
    )
}

restaurant_owner_profile_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "consent_status": "IMPLIED",
                "expired_at": "2021-09-29T00:00:00.000+00:00",
                "id": 10,
                "last_updated": "2021-03-25T00:00:00.000+00:00",
                "restaurant_id": "605b55d192c9e40e98c1877a",
                "subscribed_at": None,
                "unsubscribed_at": None,
                "user_id": 107,
                "_id": "605cbe3ee8bf2b279ae052ee"
            }
        }
    )
}


class RestaurantOwnerUpdate(serializers.Serializer):
    consent_status = serializers.ChoiceField(
        required=False, choices=ConsentStatus.choices())

    class Meta:
        ref_name = None


restaurant_owner_profile_put_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "consent_status": "EXPRESSED",
                "expired_at": None,
                "id": 10,
                "last_updated": "2021-03-25T00:00:00.000+00:00",
                "restaurant_id": "605b55d192c9e40e98c1877a",
                "subscribed_at": "2021-03-29T00:00:00.000+00:00",
                "unsubscribed_at": None,
                "user_id": 107,
                "_id": "605cbe3ee8bf2b279ae052ee"
            }
        }
    )
}
