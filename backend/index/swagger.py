from rest_framework import serializers

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response


class SendEmail(serializers.Serializer):
    subject = serializers.CharField()
    content = serializers.CharField()

    class Meta:
        ref_name = None


send_email_post_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "message": "email has been sent"
            }
        }
    )
}
