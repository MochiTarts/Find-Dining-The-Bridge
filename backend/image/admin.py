from django.db.models import Q
from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.contrib.admin.utils import model_ngettext
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse

from utils.cloud_storage import upload, delete, IMAGE, VIDEO, DEV_BUCKET
from utils.filters import NameFilter
from image.models import Image
import uuid


class imageAdmin(admin.ModelAdmin):
    list_display = ('name', 'imageUrl', 'imagePreview',
                    'uploaded_at', 'labels',)
    list_filter = (NameFilter, ('uploaded_at', DateFieldListFilter),)

    search_fields = ('labels',)

    readonly_fields = (
        "uploaded_at",
    )

    actions = ('remove_selected',)

    image_id = 0

    change_list_template = "admin/change_list_image.html"
    change_form_template = "admin/change_form_image.html"

    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        super(imageAdmin, self).__init__(model, admin_site)

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

    # modified from delete_selected (from django.contrib.admin.actions import delete_selected)
    def remove_selected(self, request, queryset):

        # Populate deletable_objects, a data structure of all related objects that will also be deleted.
        deletable_objects, model_count, perms_needed, protected = self.get_deleted_objects(
            queryset, request)

        # The user has already confirmed the deletion.
        # Do the deletion and return None to display the change list view again.
        if request.POST.get('post') and not protected:
            if perms_needed:
                raise PermissionDenied
            n = queryset.count()
            if n:
                for obj in queryset:
                    obj_display = str(obj)
                    # manually delete the images stored in the cloud
                    if obj.url:
                        try:
                            delete(obj.url)
                        except Exception:
                            continue
                    self.log_deletion(request, obj, obj_display)



                self.delete_queryset(request, queryset)
                self.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                    "count": n, "items": model_ngettext(self.opts, n)
                }, messages.SUCCESS)
            # delete all
            # queryset.delete()
            # Return None to display the change list page again.
            return None
        # intermediate confirmation view
        else:
            objects_name = model_ngettext(queryset)

            if perms_needed or protected:
                title = _("Cannot delete %(name)s") % {"name": objects_name}
            else:
                title = _("Are you sure?")

            context = {
                **self.admin_site.each_context(request),
                'title': title,
                'queryset': queryset,
                'action_checkbox_name': ACTION_CHECKBOX_NAME,
                'opts': self.opts,
                'objects_name': str(objects_name),
                'deletable_objects': [deletable_objects],
                'perms_lacking': perms_needed,
                'protected': protected,
                'model_count': dict(model_count).items(),
                'media': self.media,
            }

            request.current_app = self.admin_site.name

            # Display the confirmation page
            return TemplateResponse(request, 'admin/delete_selected_confirm_images.html',
                                    context,)

    remove_selected.allowed_permissions = ('delete',)
    remove_selected.short_description = 'remove selected Images (will remove them from the cloud)'

    def get_actions(self, request):
        actions = super().get_actions(request)
        # remove will take care the deletion (because we need to remove the image on the cloud first)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

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
