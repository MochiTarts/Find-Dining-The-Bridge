from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.utils.html import format_html
from django.db import models

from utils.cloud_storage import upload, delete, IMAGE, VIDEO, DEV_BUCKET
from utils.filters import NameFilter
from image.models import Image
import uuid

class imageAdmin(admin.ModelAdmin):
    list_display = ('name', 'imageUrl', 'imagePreview', 'uploaded_at', 'labels',)
    list_filter = (NameFilter, ('uploaded_at', DateFieldListFilter),)

    search_fields = ('labels','name',)

    readonly_fields = (
        "uploaded_at",
    )

    actions = ('remove_selected',)

    image_id = 0

    change_list_template = "admin/change_list_image.html"

    def remove_selected(self, request, obj):
        for o in obj.all():
            delete(o.url)
            o.delete()

    #delete_selected.short_description = 'remove image'


    def get_actions(self, request):
        actions = super().get_actions(request)
        # remove will take care the deletion (because we need to remove the image on the cloud first)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    
    def has_delete_permission(self, request, obj=None):
        return False

    def imageUrl(self, obj):
        return format_html("<a target='_blank' href='{url}'>{url}</a>", url=obj.url)

    imageUrl.short_description = 'image url (click to download)'

    def imagePreview(self, obj):
        #image_id = obj.url.split('/')[-1]
        self.image_id += 1
        return format_html("<button class='plus-collapsible' type='button' onclick='toggleImage({id})'>+</button><img class='img-preview' id='{id}' src='{url}'>", url=obj.url, id='img' + str(self.image_id))

    imagePreview.short_description = 'image preview'


admin.site.register(Image, imageAdmin)
