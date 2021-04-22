from rest_framework import serializers

from newsletter.models import NLUser
from subscriber_profile.enum import ConsentStatus


class NLUserInsertSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    consent_status = serializers.ChoiceField(choices=ConsentStatus.choices())

    class Meta:
        ref_name = None
