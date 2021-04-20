from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.utils import model_ngettext
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied

from login_audit.models import AuditEntry
from utils.filters import UsernameFilter, IPADDRFilter


class AuditEntryAdmin(admin.ModelAdmin):

    list_display = ('username', 'user_agent',
                    'ip_address', 'attempt_time', 'action')
    list_filter = [UsernameFilter, IPADDRFilter, 'action',
                   ('attempt_time', DateFieldListFilter)]
    actions = ('delete_all',)
    # list_per_page=200

    readonly_fields = [
        "action",
        "user_agent",
        "ip_address",
        "username",
        "http_accept",
        "path_info",
        "attempt_time",
    ]

    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        super(AuditEntryAdmin, self).__init__(model, admin_site)

    # modified from delete_selected (from django.contrib.admin.actions import delete_selected)

    def delete_all(self, request, queryset):
        # get all logs (since this action is not dependent on the selected logs)
        all_queryset = self.get_queryset(request)

        # for storing the filter arguments
        kwargs = {}
        # get all filters that is being applied on the view
        for filter, arg in request.GET.items():
            # need to make sure custom filter keywords have appropriate suffices
            if filter == 'username':
                filter = 'username__icontains'
            elif filter == 'ip_address':
                filter = 'ip_address__icontains'
            kwargs.update({filter: arg})
        # apply filters to the query set
        queryset = all_queryset.filter(**kwargs)

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
                    self.log_deletion(request, obj, obj_display)
                self.delete_queryset(request, queryset)
                self.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                    "count": n, "items": model_ngettext(self.opts, n)
                }, messages.SUCCESS)
            # delete all filtered logs
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
            return TemplateResponse(request, 'admin/delete_selected_confirm_login_all.html',
                                    context,)

    delete_all.allowed_permissions = ('delete',)
    delete_all.short_description = "Delete all filtered Loging Logs (if no filter is applied, this will delete every single log)"

    # override changelist_view to allow certain action (e.g. delete_all) to run without selecting any object

    def changelist_view(self, request, extra_context=None):
        actions = self.get_actions(request)
        if (actions and request.method == 'POST' and 'index' in request.POST and
                request.POST['action'] == 'delete_all'):

            data = request.POST.copy()
            # randomly take the first user so Django won't complain about not selecting an object when performing an action
            # there will always be at least one log because otherwise actions will not be shown
            data.update({ACTION_CHECKBOX_NAME: str(
                AuditEntry.objects.first().pk)})
            # this would select all the users
            #data['select_across'] = '1'
            request.POST = data
            response = self.response_action(
                request, queryset=self.get_queryset(request))
            if response:
                return response

        return super(AuditEntryAdmin, self).changelist_view(request, extra_context)

    # login log should not be added or changed

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(AuditEntry, AuditEntryAdmin)
