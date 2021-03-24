from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .enum import Roles
#from django import models as django_models

class SDUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=5, choices=Roles.choices(), default="BU")
    # validation purpose for a given session
    refresh_token = models.CharField(max_length=1023, default='')
    # unique id from third party
    auth_id = models.CharField(max_length=255, default='')
    # if the user is blocked by admin
    is_blocked = models.BooleanField(default=False)
    default_pwd_updated = models.NullBooleanField(default=None, editable=False)
    # reserved attribute to support interval password update policy
    pwd_update_time = models.DateTimeField(editable=False, null=True, default=None)
    # mainly for frontend to check for the existence of profile (upon login)
    profile_id = models.IntegerField(default=None)

    class Meta:
        #db_table = 'auth_user'
        verbose_name = "User"
        verbose_name_plural = "Users"
    

    def set_password(self, raw_password):
        if self.default_pwd_updated is None:
            self.default_pwd_updated = False
        
        if not self.default_pwd_updated:
            self.default_pwd_updated = True

        self.pwd_update_time = timezone.now()
        super().set_password(raw_password)

    def has_module_perms(self, app_label):
       return self.is_superuser

    def has_perm(self, perm, obj=None):
       return self.is_superuser
