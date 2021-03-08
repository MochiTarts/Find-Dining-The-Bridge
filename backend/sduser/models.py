from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .enum import Roles

class SDUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=5, choices=Roles.choices(), default="BU")
    refreshToken = models.CharField(max_length=1023, default='')
    authId = models.CharField(max_length=255, default='')

    class Meta:
        #db_table = 'auth_user'
        verbose_name = "User"
        verbose_name_plural = "Users"