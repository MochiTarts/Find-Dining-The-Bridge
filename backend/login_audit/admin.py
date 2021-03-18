from django.contrib import admin
from login_audit.models import AuditEntry
from utils.filters import UsernameFilter
from django.contrib.admin import DateFieldListFilter

class AuditEntryAdmin(admin.ModelAdmin):

    list_display = ('username', 'user_agent', 'ip_address', 'attempt_time', 'action')
    list_filter = ['action',UsernameFilter, ('attempt_time', DateFieldListFilter)]

    readonly_fields = [
        "action",
        "user_agent",
        "ip_address",
        "username",
        "http_accept",
        "path_info",
        "attempt_time",
    ]

    def has_add_permission(self, request):
        return False

admin.site.register(AuditEntry, AuditEntryAdmin)
