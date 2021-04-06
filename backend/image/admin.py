from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter

from utils.filters import NameFilter 
from image.models import Image

class imageAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'uploaded_at',)
    list_filter = (NameFilter, ('uploaded_at', DateFieldListFilter),)

    #search_fields = ('title',)

    readonly_fields = (
        "uploaded_at",
    )




admin.site.register(Image, imageAdmin)
