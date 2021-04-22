from newsletter.models import NLUser
from subscriber_profile.enum import ConsentStatus

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import serializers
from rest_framework.response import Response


class NLUserInsert(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    consent_status = serializers.ChoiceField(choices=ConsentStatus.choices())

    class Meta:
        ref_name = None


nluser_signup_post_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "first_name": "Jenny",
                "last_name": "Yu",
                "email": "something@mail.com",
                "consent_status": "EXPRESSED",
                "subscribed_at": "2021-04-20T19:54:35.362+00:00",
                "unsubscribed_at": None,
                "expired_at": None
            }
        }
    )
}

nluser_profile_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "first_name": "Bobby",
                "last_name": "Tibby",
                "email": "something2@mail.com",
                "consent_status": "IMPLIED",
                "subscribed_at": None,
                "unsubscribed_at": None,
                "expired_at": "2021-10-15T00:00:00.000+00:00"
            }
        }
    )
}
