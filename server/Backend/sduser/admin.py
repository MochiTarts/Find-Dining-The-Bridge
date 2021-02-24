from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from sduser.models import SDUser

admin.site.register(SDUser, UserAdmin)