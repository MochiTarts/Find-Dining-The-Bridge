from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import ipware.ip


def get_client_ip_address(request) -> str:
    """
    Get client IP address as configured by the user.
    The django-ipware package is used for address resolution
    """

    client_ip_address, _ = ipware.ip.get_client_ip(
        request
    )

    return client_ip_address


def get_client_user_agent(request) -> str:
    return request.META.get("HTTP_USER_AGENT", "<unknown>")[:255]


def get_client_path_info(request) -> str:
    return request.META.get("PATH_INFO", "<unknown>")[:255]


def get_client_http_accept(request) -> str:
    return request.META.get("HTTP_ACCEPT", "<unknown>")[:1025]


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    user_agent = models.CharField(
        _("user agent"), max_length=255, db_index=True)
    ip_address = models.GenericIPAddressField(
        _("ip address"), null=True, db_index=True)
    username = models.CharField(
        _("username"), max_length=255, null=True, db_index=True)
    http_accept = models.CharField(_("http accept"), max_length=1025)
    path_info = models.CharField(_("path"), max_length=255)
    attempt_time = models.DateTimeField(_("attempt time"), auto_now_add=True)

    def __unicode__(self):
        return '[{0}] {1} - {2} ({3})'.format(self.action, self.username, self.ip_address, self.attempt_time)

    def __str__(self):
        return '[{0}] {1} - {2} ({3})'.format(self.action, self.username, self.ip_address, self.attempt_time)

    class Meta:
        verbose_name = 'Login Log'
        ordering = ["-attempt_time"]


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """
    log.info('login user: {user} via ip: {ip}'.format(
        user=user,
        ip=get_client_ip_address(request)
    ))
    """
    AuditEntry.objects.create(
        action='logged in',
        username=user.username,
        attempt_time=timezone.now(),
        user_agent=get_client_user_agent(request),
        ip_address=get_client_ip_address(request),
        path_info=get_client_path_info(request),
        http_accept=get_client_http_accept(request)
    )


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """
    log.info('logout user: {user} via ip: {ip}'.format(
        user=user,
        ip=get_client_ip_address(request)
    ))
    """
    AuditEntry.objects.create(
        action='logged out',
        username=user.username,
        attempt_time=timezone.now(),
        user_agent=get_client_user_agent(request),
        ip_address=get_client_ip_address(request),
        path_info=get_client_path_info(request),
        http_accept=get_client_http_accept(request)
    )


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    """
    log.info('login failed for: {credentials}'.format(
        credentials=credentials,
    ))
    """
    # request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
    AuditEntry.objects.create(
        action='login failed',
        username=credentials.get('username', None),
        attempt_time=timezone.now(),
    )
