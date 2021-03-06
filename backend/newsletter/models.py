#from django.db import models
from djongo import models
#from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator, validate_email
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
from django.db import IntegrityError
from rest_framework.exceptions import NotFound

from subscriber_profile.enum import ConsentStatus
from utils.validators import check_script_injections, validate_name, validate_url, validate_postal_code
from utils.model_util import save_and_clean, update_model_geo, model_refresh

from datetime import date, datetime
from bson import ObjectId
import requests
import json
import ipware.ip

FOOD_PICTURE = 'https://storage.googleapis.com/default-assets/no-image.png'

RESTAURANT_COVER = 'https://storage.googleapis.com/default-assets/cover.jpg'
RESTAURANT_LOGO = 'https://storage.googleapis.com/default-assets/logo.jpg'
DISHES = 'dishes.csv'


class NLUser(models.Model):
    """ Scarborough Dining Newsletter User """
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(primary_key=True, default='')
    consent_status = models.CharField(
        max_length=30, choices=ConsentStatus.choices(), default="IMPLIED")
    subscribed_at = models.DateField(blank=True, default=None)
    unsubscribed_at = models.DateField(blank=True, default=None)
    expired_at = models.DateField(blank=True, default=None)

    @classmethod
    def signup(cls, first_name, last_name, email, consent_status, expired_at):
        """ Constructs & Saves User to DB returning the newly signed up user object

        :param first_name: first name of user
        :type first_name: str
        :param last_name: last name of user
        :type last_name: str
        :param email: email of user
        :type email: str
        :param consent_status: consent status regarding user's choice of receiving project updates
        :type consent_stautus: str
        :return: new NLUser
        :rtype: :class:`NLUser` object
        """

        if cls.objects.filter(email=email).exists():
            raise IntegrityError("This email has already been used.")
        user = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            consent_status=consent_status
        )
        if consent_status == ConsentStatus.EXPRESSED.name:
            user.subscribed_at = date.today()
        else:
            user.expired_at = expired_at
        user = save_and_clean(user)
        return user

    @classmethod
    def get(email):
        """ Retrieves the newsletter user

        :param email: email of newsletter user
        :type email: str
        :raises NotFound: if user is not found
        :return: the NLUser record of email
        :rtype: :class: `NLUser`
        """
        nluser_filter = NLUser.objects.filter(email=email)
        if nluser_filter.count() > 1:
            raise MultipleObjectsReturned(
                "Received multiple records of NLUser with email: "+email)
        if not nluser_filter.first():
            raise NotFound("Cannot find NLUser with email: "+email)
        return nluser_filter.first()

    @classmethod
    def field_validate(self, fields):
        """ Validates fields

        :param fields: Dictionary of fields to validate
        :return: A list of fields that were invalid. Returns None if all fields are valid
        """
        user_urls = ['picture']

        invalid = {'Invalid': []}

        if 'first_name' in fields:
            try:
                validate_name(fields['first_name'])
            except ValidationError as e:
                invalid['Invalid'].append('first_name')
        else:
            invalid['Invalid'].append('first_name')

        if 'last_name' in fields:
            try:
                validate_name(fields['last_name'])
            except ValidationError as e:
                invalid['Invalid'].append('last_name')
        else:
            invalid['Invalid'].append('last_name')

        if 'email' in fields:
            try:
                validate_email(fields['email'])
            except ValidationError as e:
                invalid['Invalid'].append('email')
        else:
            invalid['Invalid'].append('email')

        if invalid['Invalid']:
            raise ValidationError(message=invalid, code="invalid_input")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Consumer'
        verbose_name_plural = "Consumers"


class NLAudit(models.Model):
    """ signup audit to prevent spam"""
    ip = models.CharField(max_length=50, default='')
    last_signup_time = models.DateField(blank=True, default=None)
    temp_blocked = models.BooleanField(blank=True, default=False)
    count_daily = models.IntegerField(blank=True, default=0)
    count = models.IntegerField(blank=True, default=0)
    perm_blocked = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name = 'Signup Log'
        verbose_name_plural = "Signup Logs (count/ip)"
        ordering = ["-last_signup_time"]

    def __str__(self):
        return '{0}: {1}'.format(self.ip, self.count)

    @classmethod
    def update_audit(self, ip):
        audit_log, created = NLAudit.objects.get_or_create(ip=ip)

        if created:
            audit_log.count_daily = 1
            audit_log.count = 1
            audit_log.last_signup_time = timezone.now()
            audit_log.save()
        # update existing
        else:
            if (timezone.localdate() - audit_log.last_signup_time).days < 1:
                audit_log.count_daily = audit_log.count_daily + 1
            else:
                audit_log.count_daily = 1
            audit_log.count = audit_log.count + 1
            audit_log.last_signup_time = timezone.now()
            if audit_log.count_daily > 100:
                audit_log.temp_blocked = True
            elif audit_log.count > 2000:
                audit_log.perm_blocked = True
            elif audit_log.temp_blocked:
                audit_log.temp_blocked = False

            audit_log.save()

            if audit_log.perm_blocked:
                return True

        return audit_log.temp_blocked
