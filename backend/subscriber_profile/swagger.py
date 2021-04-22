from subscriber_profile.models import SubscriberProfile
from subscriber_profile.enum import ConsentStatus

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.response import Response
from rest_framework import serializers


class SubscriberProfileInsert(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    postalCode = serializers.CharField(max_length=7)
    phone = serializers.IntegerField()
    consent_status = serializers.ChoiceField(
        required=False, choices=ConsentStatus.choices())

    class Meta:
        ref_name = None


subscriber_profile_signup_post_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 43.781841, 'lng': -79.1880063}",
                "consent_status": "IMPLIED",
                "first_name": "Bob",
                "expired_at": "2021-09-29T00:00:00.000+00:00",
                "last_name": "Smith",
                "id": 10,
                "last_updated": "2021-03-25T00:00:00.000+00:00",
                "phone": 1234567890,
                "postalCode": "M1C 1A4",
                "subscribed_at": None,
                "unsubscribed_at": None,
                "user_id": 113,
                "_id": "605a434ca05efe8d91ef8120"
            }
        }
    )
}

subscriber_profile_profile_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 43.781841, 'lng': -79.1880063}",
                "consent_status": "IMPLIED",
                "first_name": "Bob",
                "expired_at": "2021-09-29T00:00:00.000+00:00",
                "last_name": "Smith",
                "id": 10,
                "last_updated": "2021-03-25T00:00:00.000+00:00",
                "phone": 1234567890,
                "postalCode": "M1C 1A4",
                "subscribed_at": None,
                "unsubscribed_at": None,
                "user_id": 113,
                "_id": "605a434ca05efe8d91ef8120"
            }
        }
    )
}


class SubscriberProfileUpdate(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    postalCode = serializers.CharField(max_length=7, required=False)
    phone = serializers.IntegerField()
    consent_status = serializers.ChoiceField(
        required=False, choices=ConsentStatus.choices())

    class Meta:
        ref_name = None


subscriber_profile_profile_put_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 43.781841, 'lng': -79.1880063}",
                "consent_status": "IMPLIED",
                "first_name": "Bobby",
                "expired_at": "2021-09-29T00:00:00.000+00:00",
                "last_name": "Smithers",
                "id": 10,
                "last_updated": "2021-03-25T00:00:00.000+00:00",
                "phone": 1234567890,
                "postalCode": "M1C 1A4",
                "subscribed_at": None,
                "unsubscribed_at": None,
                "user_id": 113,
                "_id": "605a434ca05efe8d91ef8120"
            }
        }
    )
}
