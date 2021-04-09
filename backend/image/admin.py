from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.utils.html import format_html
from django.db.models import Q

from utils.cloud_storage import upload, delete, IMAGE, VIDEO, DEV_BUCKET
from utils.filters import NameFilter
from image.models import Image
import uuid

class imageAdmin(admin.ModelAdmin):
    list_display = ('name', 'imageUrl', 'imagePreview', 'uploaded_at', 'labels',)
    list_filter = (NameFilter, ('uploaded_at', DateFieldListFilter),)

    search_fields = ('labels',)

    readonly_fields = (
        "uploaded_at",
    )

    actions = ('remove_selected',)

    image_id = 0

    change_list_template = "admin/change_list_image.html"
    change_form_template = "admin/change_form_image.html"

    # override get_search_results to search by csv labels
    def get_search_results(self, request, queryset, search_term):
        #queryset, use_distinct = super(imageAdmin, self).get_search_results(request, queryset, search_term)
        use_distinct = False
        if search_term != '':
            labels = search_term.split(',')
            qs = Q(labels__icontains=labels[0].strip())
            for label in labels[1:]:
                qs |= Q(labels__icontains=label.strip())
            queryset |= self.model.objects.filter(qs)

        return queryset, use_distinct

    def remove_selected(self, request, obj):
        count = 0
        for o in obj.all():
            if o.url:
                delete(o.url)
            o.delete()
            count += 1
        if count > 1:
            messages.success(request, "Successfully removed " + str(count) + " images.")
        elif count == 1:
            messages.success(request, "Successfully removed " + str(count) + " image.")
        else:
            messages.info(request, 'No image has been removed')
    
    remove_selected.short_description = 'remove selected image(s)'


    def get_actions(self, request):
        actions = super().get_actions(request)
        # remove will take care the deletion (because we need to remove the image on the cloud first)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    
    def has_delete_permission(self, request, obj=None):
        return False

    def imageUrl(self, obj):
        # clickable url (for download) with clickboard symbol (for copy)
        return format_html("<a target='_blank' href='{url}'>{url}</a> <span class='clickboard' onclick='copyToClipboard(\"{url}\")'>&#128203;</span>", url=obj.url)

    imageUrl.short_description = 'image url (click to download)'

    def imagePreview(self, obj):
        #image_id = obj.url.split('/')[-1]
        self.image_id += 1
        return format_html("<button class='plus-collapsible' type='button' onclick='toggleImage({id})'>+</button><img class='img-preview' id='{id}' src='{url}'>", url=obj.url, id='img' + str(self.image_id))

    imagePreview.short_description = 'image preview'



admin.site.register(Image, imageAdmin)
