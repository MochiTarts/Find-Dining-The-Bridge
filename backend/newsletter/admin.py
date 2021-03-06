from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.http import HttpResponse
from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.utils import model_ngettext
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied

from newsletter.models import NLUser, NLAudit
from utils.filters import EmailFilter, IPFilter
from utils.model_util import model_to_json

from collections import OrderedDict
import datetime


class NLUserAdmin(admin.ModelAdmin):
    """ Admin Model for Newsletter Signup """
    list_filter = ('consent_status', EmailFilter,)
    list_display = ('first_name', 'last_name', 'email', 'consent_status',
                    'subscribed_at', 'unsubscribed_at', 'expired_at',)
    list_display_links = ('first_name', 'last_name', 'email',)
    readonly_fields = ('email',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        # reverse the action list so delete comes latest
        actions = OrderedDict(reversed(list(actions.items())))
        return actions

    # override changelist_view to allow certain action (e.g. generate google sheet) to run without selecting any object

    def changelist_view(self, request, extra_context=None):
        actions = self.get_actions(request)
        if (actions and request.method == 'POST' and 'index' in request.POST and
                request.POST['action'] == 'generate_google_spreadsheet'):
            data = request.POST.copy()
            # randomly take the first user so Django won't complain about not selecting an object when performing an action
            data.update({ACTION_CHECKBOX_NAME: str(NLUser.objects.first().pk)})
            # this would select all the users
            #data['select_across'] = '1'
            request.POST = data
            response = self.response_action(
                request, queryset=self.get_queryset(request))
            if response:
                return response

        return super(NLUserAdmin, self).changelist_view(request, extra_context)


class NLAuditAdmin(admin.ModelAdmin):
    """ Admin Model for Signup Audit """
    list_display = ('ip', 'count_daily', 'count',
                    'last_signup_time', 'temp_blocked', 'perm_blocked', )

    list_filter = [IPFilter, 'temp_blocked', 'perm_blocked',
                   ('last_signup_time', DateFieldListFilter)]

    actions = ('delete_all',)
    # list_per_page=200

    readonly_fields = [
        "ip",
        "last_signup_time",
    ]

    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        super(NLAuditAdmin, self).__init__(model, admin_site)

    # modified from delete_selected (from django.contrib.admin.actions import delete_selected)
    def delete_all(self, request, queryset):
        # get all logs (since this action is not dependent on the selected logs)
        all_queryset = self.get_queryset(request)
        # for storing the filter arguments
        kwargs = {}
        # get all filters that is being applied on the view
        for filter, arg in request.GET.items():
            # need to make sure custom filter keywords have appropriate suffices
            if filter == 'ip':
                filter = 'ip__icontains'
            # skip search field if it is enabled, need to handle it if search field is required
            elif filter == 'q':
                continue
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
    delete_all.short_description = "Delete all filtered Newsletter Logs (if no filter is applied, this will delete every single log)"

    # override changelist_view to allow certain action (e.g. delete_all) to run without selecting any object

    def changelist_view(self, request, extra_context=None):
        actions = self.get_actions(request)
        if (actions and request.method == 'POST' and 'index' in request.POST and
                request.POST['action'] == 'delete_all'):

            data = request.POST.copy()
            # randomly take the first user so Django won't complain about not selecting an object when performing an action
            # there will always be at least one log because otherwise actions will not be shown
            data.update({ACTION_CHECKBOX_NAME: str(
                NLAudit.objects.first().pk)})
            # this would select all the users
            #data['select_across'] = '1'
            request.POST = data
            response = self.response_action(
                request, queryset=self.get_queryset(request))
            if response:
                return response

        return super(NLAuditAdmin, self).changelist_view(request, extra_context)


admin.site.register(NLUser, NLUserAdmin)
admin.site.register(NLAudit, NLAuditAdmin)
