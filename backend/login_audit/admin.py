from django.contrib import admin
from login_audit.models import AuditEntry
from utils.filters import UsernameFilter
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import messages


class AuditEntryAdmin(admin.ModelAdmin):

    list_display = ('username', 'user_agent', 'ip_address', 'attempt_time', 'action')
    list_filter = ['action',UsernameFilter, ('attempt_time', DateFieldListFilter)]
    actions = ('delete_all',)
    #list_per_page=200

    readonly_fields = [
        "action",
        "user_agent",
        "ip_address",
        "username",
        "http_accept",
        "path_info",
        "attempt_time",
    ]

    def delete_all(self, request, queryset):
        # get all logs (since this action is not dependent on the selected logs)
        all_queryset = self.get_queryset(request)
        # for storing the filter arguments
        kwargs = {}
        # get all filters that is being applied on the view
        for filter,arg in request.GET.items():
            kwargs.update({filter:arg})
        # apply filters to the query set
        queryset = all_queryset.filter(**kwargs)
        # delete all filtered logs
        queryset.delete()

    delete_all.short_description = "delete all filtered Loging Logs"


    # override changelist_view to allow certain action (e.g. delete_all) to run without selecting any object
    def changelist_view(self, request, extra_context=None):
        actions = self.get_actions(request)
        if (actions and request.method == 'POST' and 'index' in request.POST and
                request.POST['action'] == 'delete_all'):
            
            data = request.POST.copy()
            # randomly take the first user so Django won't complain about not selecting an object when performing an action
            # there will always be at least one log because otherwise actions will not be shown
            data.update({ACTION_CHECKBOX_NAME: str(AuditEntry.objects.first().pk)})
            # this would select all the users
            #data['select_across'] = '1'
            request.POST = data
            response = self.response_action(request, queryset=self.get_queryset(request))
            if response:
                return response

        return super(AuditEntryAdmin, self).changelist_view(request, extra_context)



    def has_add_permission(self, request):
        return False

admin.site.register(AuditEntry, AuditEntryAdmin)
