from django.contrib.auth.models import AbstractUser

class SDUser(AbstractUser):
    class Meta:
        #db_table = 'auth_user'
        verbose_name = "User"
        verbose_name_plural = "Users"