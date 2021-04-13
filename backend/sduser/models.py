from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .enum import Roles
#from django import models as django_models

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
#from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

class SDUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=5, choices=Roles.choices(), default="BU")
    # validation purpose for a given session
    refresh_token = models.CharField(max_length=1023, default='', blank=True, help_text=_(
            'This is for authentication purpose.'
        ),)
    # unique id from third party
    auth_id = models.CharField(max_length=255, default='', blank=True, help_text=_(
            'This is a unique id given by third parties '
            '(if the user logs in with a third party service)'
        ),)
    # if the user is blocked by admin
    is_blocked = models.BooleanField(default=False, help_text=_(
            'Select this to block the user from accessing the site. '
        ),)
    default_pwd_updated = models.NullBooleanField(default=None, editable=False)
    # reserved attribute to support interval password update policy
    pwd_update_time = models.DateTimeField(editable=False, null=True, blank=True, default=None)
    # mainly for frontend to check for the existence of profile (upon login)
    profile_id = models.IntegerField(default=None, null=True, blank=True)
    # override default is_active field to have it default to false
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'If this field is not selected, a verification email will be send to the user. '
            'Unselect this instead of deleting accounts.'
        ),
    )

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

@receiver(pre_delete, sender=SDUser)
def delete_user(sender, instance, **kwargs):
    print(sender)
    if instance.is_superuser:
        raise PermissionDenied