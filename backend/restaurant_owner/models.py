from django.core.validators import URLValidator, validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models, IntegrityError
from rest_framework.exceptions import NotFound

from restaurant_owner.enum import ConsentStatus
from restaurant.models import PendingRestaurant
#from subscriber_profile.enum import ConsentStatus
from utils.validators import check_script_injections, validate_name, validate_url
from utils.model_util import save_and_clean, edit_model

from bson import ObjectId
import datetime
import requests

restaurant_owner_editable = [
    "restaurant_id", "last_updated",
    "consent_status", "subscribed_at",
    "unsubscribed_at", "expired_at"
]


class RestaurantOwner(models.Model):
    """ Find Dining Restaurant Owner profile model """
    user_id = models.IntegerField(default=None)
    restaurant_id = models.CharField(max_length=24, blank=True, default="")
    last_updated = models.DateField(auto_now=True)
    consent_status = models.CharField(
        max_length=30, choices=ConsentStatus.choices(), default='IMPLIED', blank=True)
    subscribed_at = models.DateField(blank=True)
    unsubscribed_at = models.DateField(blank=True)
    expired_at = models.DateField(blank=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    def signup(cls, restaurant_owner_data: dict):
        """ Constructs and saves a new RestaurantOwner record to the database and
        returns the newly made RestaurantOwner object

        :param restaurant_owner_data: data of the restaurant owner
        :type restaurant_owner_data: dict
        :rairses ObjectDoesNotExist: if PendingRestaurant record
            of given id does not exist
        :raises IntegrityError: upon business logic violations
        :return: new RestaurantOwner object
        """
        user_id = restaurant_owner_data['user_id']
        restaurant_id = restaurant_owner_data['restaurant_id']

        if cls.objects.filter(user_id=user_id).exists():
            raise IntegrityError(
                'Cannot insert restaurant owner user, a user with this user_id already exists')
        restaurant_filter = PendingRestaurant.objects.filter(_id=restaurant_id)
        if not restaurant_filter.exists():
            raise ObjectDoesNotExist(
                "This restaurant with _id: "+restaurant_id+" does not exist")

        if "consent_status" in restaurant_owner_data:
            restaurant_owner_data.update(
                handleConsentStatus(restaurant_owner_data['consent_status']))

        restaurant = restaurant_filter.first()
        restaurant.owner_user_id = user_id
        save_and_clean(restaurant)

        profile = cls(**restaurant_owner_data)
        profile = save_and_clean(profile)
        return profile

    @classmethod
    def get_by_user_id(cls, user_id):
        """ Retrieves a RestaurantOwner record given 
        the user_id

        :param user_id: id of the sduser
        :type user_id: int
        :raises NotFound: when the RestaurantOwner record does not exist
            or the SDUser record does not exist
        :return: the RestaurantOwner record
        :rtype: :class: `RestaurantOwner`
        """
        ro_filter = RestaurantOwner.objects.filter(user_id=user_id)
        if not ro_filter.exists():
            raise NotFound(
                "The restaurant owner profile with user_id: "+str(user_id)+" does not exist")
        if ro_filter.count() > 1:
            raise MultipleObjectsReturned(
                "There are more than one restaurant owner record with this user_id: "+str(user_id))

        return ro_filter.first()

    @classmethod
    def edit_profile(cls, user_id, user_data):
        """ Updates the fields of a RestaurantOwner record of the user_id
        Updated fields and values are contained in the user_data dict

        :param user_id: id of the sduser
        :type user_id: int
        :param user_data: RestaurnatOwner fields and values to be updated to
        :type user_data: dict
        :raises ObjectDoesNotExist: when SDUser or RestaurantOwner record
            does not exist
        :return: the updated RestaurantOwner record
        :rtype: :class: `RestaurantOwner`
        """
        ro_filter = RestaurantOwner.objects.filter(user_id=user_id)
        profile = ro_filter.first()

        edit_model(profile, user_data, restaurant_owner_editable)
        if "consent_status" in user_data:
            consent_data = handleConsentStatus(user_data["consent_status"])
            for field in consent_data:
                setattr(profile, field, consent_data[field])
        profile = save_and_clean(profile)
        return profile

    @classmethod
    def field_validate(self, fields):
        """ Validates the fields of the request to insert
        or modify a RestaurantOwner object

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

        if 'restaurant_id' in fields:
            try:
                ObjectId(fields['restaurant_id'])
            except Exception:
                invalid['Invalid'].append('restaurant_id')

        if 'last_updated' in fields:
            try:
                datetime.datetime.strptime(fields['last_updated'], '%Y-%m-%d')
            except ValueError:
                invalid['Invalid'].append(
                    'last_updated (format should be YYYY-MM-DD)')

        if 'expired_at' in fields:
            try:
                datetime.datetime.strptime(fields['last_updated'], '%Y-%m-%d')
            except ValueError:
                invalid['Invalid'].append(
                    'expired_at (format should be YYYY-MM-DD)')

        if invalid['Invalid']:
            raise ValidationError(message=invalid, code="invalid_input")

    class Meta:
        verbose_name = 'Restaurant Owner'


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
