from django.db import models
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from utils.common import save_and_clean
from utils.validators import check_script_injections, validate_postal_code, validate_name
from utils.geo_controller import geocode

from .enum import ConsentStatus

import datetime

User = get_user_model()

class SubscriberProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.BigIntegerField(blank=True, default=None)
    postalCode = models.CharField(max_length=7, blank=True, default='')
    GEO_location = models.CharField(
        max_length=50, blank=True, default='')
    last_updated = models.DateField(auto_now=True, blank=True)
    consent_status = models.CharField(
        max_length=12, choices=ConsentStatus.choices(), default='IMPLIED', blank=True)
    expired_at = models.DateField(blank=True)
    subscribed_at = models.DateField(blank=True)
    unsubscribed_at = models.DateField(blank=True)
    
    class Meta:
        db_table = 'subscriber_profile'

    @classmethod
    def field_validate(self, fields):
        """ Validates fields

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :return: A list of fields that were invalid. Returns None if all fields are valid
        :rtype: json
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
            invalid['Invalid'].append("user_id must be passed and be equal to the user's id")
        elif User.objects.get(pk=fields['user_id']) == None:
            invalid['Invalid'].append("SDUser with this user_id does not exist")

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

        if 'postalCode' in fields and fields['postalCode'] is not None:
            try:
                validate_postal_code(fields['postalCode'])
            except ValidationError as e:
                invalid['Invalid'].append('postalCode')

        if not invalid['Invalid']:
            return None
        else:
            return invalid

    @classmethod
    def signup(cls, subscriber_data:dict):
        """ Constructs and saves SubscriberProfile to database returning the newly created profile

        :param subscriber_data: data of the subscriber
        :subscriber_data: dict
        :return: SubscriberProfile Object
        :rtype: :class:`SubscriberProfile`
        """
        invalid = SubscriberProfile.field_validate(subscriber_data)
        if not invalid:
            if "consent_status" in subscriber_data:
                subscriber_data.update(handleConsentStatus(subscriber_data['consent_status']))
            profile = cls(**subscriber_data)
            profile.GEO_location = geocode(profile.postalCode)
            profile = save_and_clean(profile)
            return profile
        else:
            raise ValidationError(
                'Validation error. Please check the following: ' + str(print(invalid)))

    @classmethod
    def edit(cls, subscriber_data):
        """
        Edits current SubscriberProfile in DB returning the edited profile
        :param subscriber_data: json data of the subscriber
        :return: SubscriberProfile Object
        """
        invalid = SubscriberProfile.field_validate(subscriber_data)

        if not invalid:
            profile = SubscriberProfile.objects.get(pk=subscriber_data['user_id'])
            for field in subscriber_data:
                setattr(profile, field, subscriber_data[field])
            profile.GEO_location = geocode(profile.postalCode)
            profile = save_and_clean(profile)
            return profile
        else:
            raise ValidationError(
                'Validation error. Please check the following: ' + str(print(invalid)))

def handleConsentStatus(consent_status):
    profile = {}
    profile["consent_status"] = consent_status
    if consent_status == "EXPRESSED":
        profile["expired_at"] =  None
        profile["subscribed_at"] = datetime.datetime.today()
        profile["unsubscribed_at"] = None
    elif consent_status == "IMPLIED":
        profile["expired_at"] = datetime.datetime.today() + datetime.timedelta(days=+182)
        profile["subscribed_at"] = None
        profile["unsubscribed_at"] = None
    return profile