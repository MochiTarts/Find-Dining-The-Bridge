from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class SDUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    class Meta:
        #db_table = 'auth_user'
        verbose_name = "User"
        verbose_name_plural = "Users"