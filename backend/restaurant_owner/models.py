from django.core.validators import URLValidator, validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models

from restaurant_owner.enum import ConsentStatus
#from subscriber_profile.enum import ConsentStatus
from utils.validators import check_script_injections, validate_name, validate_url
from utils.model_util import save_and_clean

from bson import ObjectId
import datetime
import requests

class RestaurantOwner(models.Model):
    """ Find Dining Restaurant Owner profile model """
    user_id = models.IntegerField(default=None)
    restaurant_id = models.CharField(max_length=24, blank=True, default="")
    last_updated = models.DateField(auto_now=True)
    consent_status = models.CharField(max_length=30, choices=ConsentStatus.choices(), default='IMPLIED', blank=True)
    subscribed_at = models.DateField(blank=True)
    unsubscribed_at = models.DateField(blank=True)
    expired_at = models.DateField(blank=True)

    @classmethod
    def signup(cls, restaurant_owner_data:dict):
        """ Constructs and saves restaurant owner to the database and
        returns the newly registered restaurant owner object

        :param: restaurant_owner_data: data of the restaurant owner
        :return: new RestaurantOwner object
        """
        if not cls.objects.filter(user_id=restaurant_owner_data['user_id']).exists():
            if "consent_status" in restaurant_owner_data:
                restaurant_owner_data.update(handleConsentStatus(subscriber_data['consent_status']))
            profile = cls(**restaurant_owner_data)
            profile = save_and_clean(profile)
            return profile
        else:
            raise ValueError('Cannot insert restaurant owner user, a user with this email already exists')

    @classmethod
    def field_validate(self, fields):
        """ Validates the fields of the request to insert or modify a RestaurantOwner object

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

        if 'restaurant_id' in fields:
            try:
                ObjectId(fields['restaurant_id'])
            except Exception:
                invalid['Invalid'].append('restaurant_id')

        if 'last_updated' in fields:
            try:
                datetime.datetime.strptime(fields['last_updated'], '%Y-%m-%d')
            except ValueError:
                invalid['Invalid'].append('last_updated (format should be YYYY-MM-DD)')

        if 'expired_at' in fields:
            try:
                datetime.datetime.strptime(fields['last_updated'], '%Y-%m-%d')
            except ValueError:
                invalid['Invalid'].append('expired_at (format should be YYYY-MM-DD)')

        if not invalid['Invalid']:
            return None
        else:
            return invalid

    class Meta:
        verbose_name = 'Restaurant Owner'

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