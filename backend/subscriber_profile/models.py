from django.db import models
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from utils.common import save_and_clean
from utils.validators import check_script_injections, validate_postal_code, validate_name
from utils.geo_controller import geocode
from subscriber_profile.enum import ConsentStatus

import datetime

User = get_user_model()


class SubscriberProfile(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=30, default="", blank=True)
    last_name = models.CharField(max_length=150, default="", blank=True)
    phone = models.BigIntegerField(null=True, default=None, blank=True)
    phone_ext = models.BigIntegerField(blank=True, null=True)
    postalCode = models.CharField(max_length=7, default='', blank=True)
    GEO_location = models.CharField(
        max_length=50, default='')
    last_updated = models.DateField(auto_now=True, null=True, editable=False)
    consent_status = models.CharField(
        max_length=12, choices=ConsentStatus.choices(), default='IMPLIED')
    expired_at = models.DateField(null=True, blank=True)
    subscribed_at = models.DateField(null=True, blank=True)
    unsubscribed_at = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'subscriber_profile'

    def __str__(self):
        return str(self.id)

    @classmethod
    def field_validate(self, fields):
        """ Validates fields

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :raises: ValidationError when there are invalid(s)
        :return: None
        """

        invalid = {'Invalid': []}
        # check if there is script in any field values
        for attr in fields:
            value = fields[attr]
            if value is not None:
                try:
                    check_script_injections(value)
                except ValidationError as e:
                    invalid['Invalid'].append(attr)

        if 'user_id' not in fields:
            invalid['Invalid'].append(
                "user_id must be passed and be equal to the user's id")
        elif User.objects.get(pk=fields['user_id']) == None:
            invalid['Invalid'].append(
                "SDUser with this user_id does not exist")

        if 'first_name' in fields:
            try:
                validate_name(fields['first_name'])
            except ValidationError as e:
                invalid['Invalid'].append('first_name')

        if 'last_name' in fields:
            try:
                validate_name(fields['last_name'])
            except ValidationError as e:
                invalid['Invalid'].append('last_name')

        if 'expired_at' in fields:
            try:
                datetime.datetime.strptime(fields['last_updated'], '%Y-%m-%d')
            except ValueError:
                invalid['Invalid'].append(
                    'expired_at (format should be YYYY-MM-DD)')

        if 'phone' in fields and fields['phone'] is not None:
            if len(str(fields['phone'])) != 10 and str(fields['phone']).isnumeric():
                invalid['Invalid'].append('phone')

        if 'postalCode' in fields:
            if not fields['postalCode']:
                invalid['Invalid'].append('postalCode')
            else:
                try:
                    validate_postal_code(fields['postalCode'])
                    geocode(fields['postalCode'])
                except ValidationError:
                    invalid['Invalid'].append('postalCode')

        if invalid['Invalid']:
            raise ValidationError(message=invalid, code="invalid_input")

    @classmethod
    def signup(cls, subscriber_data):
        """ Constructs and saves SubscriberProfile to database returning the newly created profile

        :param subscriber_data: data of the subscriber
        :subscriber_data: dict
        :return: SubscriberProfile Object
        :rtype: :class:`SubscriberProfile`
        """
        SubscriberProfile.field_validate(subscriber_data)

        if "consent_status" in subscriber_data:
            subscriber_data.update(handleConsentStatus(
                subscriber_data['consent_status']))
        profile = cls(**subscriber_data)
        profile.GEO_location = geocode(profile.postalCode)
        profile = save_and_clean(profile)
        return profile

    @classmethod
    def edit(cls, subscriber_data):
        """
        Edits current SubscriberProfile in DB returning the edited profile
        :param subscriber_data: json data of the subscriber
        :return: SubscriberProfile Object
        """
        SubscriberProfile.field_validate(subscriber_data)
        profile = SubscriberProfile.objects.get(
            user_id=subscriber_data['user_id'])
        if not profile:
            raise ObjectDoesNotExist(
                'No subscriber profile found with owner user id of this: ' + subscriber_data['user_id'])

        for field in subscriber_data:
            setattr(profile, field, subscriber_data[field])
        profile.GEO_location = geocode(profile.postalCode)
        if "consent_status" in subscriber_data:
            consent_data = handleConsentStatus(
                subscriber_data["consent_status"])
            for field in consent_data:
                setattr(profile, field, consent_data[field])
        profile = save_and_clean(profile)
        return profile


def handleConsentStatus(consent_status):
    """ Creates a dict containing the fields and values
    related to a user's consent status.

    :param consent_status: the consent status value (ie. 'EXPRESSED', 'IMPLIED')
    :type consent_status: str
    :return: a dict containing the fields and values depending on the given
            consent_status
    :rtype: dict
    """

    profile = {}
    profile["consent_status"] = consent_status
    if consent_status == "EXPRESSED":
        profile["subscribed_at"] = datetime.datetime.today()
    elif consent_status == "IMPLIED":
        profile["expired_at"] = datetime.datetime.today() + \
            datetime.timedelta(days=+182)
    elif consent_status == "UNSUBSCRIBED":
        profile["unsubscribed_at"] = datetime.datetime.today()
    return profile
