from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import BadHeaderError
from django.utils.html import format_html
from django.urls import reverse
from django import forms

from sduser.forms import AdminForm
from sduser.utils import send_email_verification, send_email_deactivate_notify
from utils.filters import InputFilter, EmailFilter, UsernameFilter
from utils.model_util import model_to_json

from smtplib import SMTPException
from collections import OrderedDict

import copy

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'activated', 'is_active', 'is_blocked', 'role',
                    'is_staff', 'is_superuser', 'last_login', 'pwd_update_time')
    list_filter = (EmailFilter, UsernameFilter, 'is_staff',
                   'is_superuser', 'is_blocked',)
    # note that the order of actions will be reversed (in get_actions)
    actions = ('disable_user','disable_user_notify','enable_user','email_verification', 'unblock_user', 'block_user',)
    # list_per_page=200

    readonly_fields = (
        "last_login",
        "pwd_update_time",
    )

    class Meta:
        # for some reason setting this is not enough, need to override get_form as well
        form = AdminForm

    def get_form(self, request, obj=None, **kwargs):
        """
        overrode get_form to apply field logics
        """
        kwargs['form'] = AdminForm
        form = super().get_form(request, obj, **kwargs)

        if 'change' in kwargs:
            # copy the form to avoid change by reference
            form = copy.deepcopy(form)

            first_name_field = form.base_fields['first_name']
            last_name_field = form.base_fields['last_name']
            # hide first name and last name field as we are not using them
            # but they are inherited from abstractUser
            first_name_field.widget = forms.HiddenInput()
            last_name_field.widget = forms.HiddenInput()
            # if editing
            # if kwargs['change']:

        return form

    # make auth_id and refresh_token field read only on creation
    def get_readonly_fields(self, request, obj=None):
        # creating a user
        if not obj:
            return self.readonly_fields + ("auth_id", "refresh_token",)
        return self.readonly_fields

    def get_actions(self, request):
        actions = super().get_actions(request)
        # reverse the action list so delete comes latest
        actions = OrderedDict(reversed(list(actions.items())))
        return actions

    def block_user(self, request, queryset):
        try:
            queryset.update(is_blocked=True)
            msg = "Selected Users have been blocked."
            messages.success(request, msg)
        except Exception:
            msg = "Fail to block one or more Users"
            messages.error(request, msg)

    block_user.short_description = "Block selected Users"

    def unblock_user(self, request, queryset):
        try:
            queryset.update(is_blocked=False)
            msg = "Selected Users have been unblocked."
            messages.success(request, msg)
        except Exception:
            msg = "Fail to unblock one or more Users"
            messages.error(request, msg)

    unblock_user.short_description = "Unblock selected Users"

    def enable_user(self, request, queryset):
        try:
            count = queryset.update(is_active=True)
            if count > 1:
                msg = "Selected " + str(count) + " Users have been enabled."
            else:
                msg = "Selected User has been enabled."
            messages.success(request, msg)
        except Exception:
            msg = "Fail to enable one or more Users"
            messages.error(request, msg)

    enable_user.short_description = "Enable selected Users to access the site (skip email verification)"

    def disable_user_notify(self, request, queryset):
        try:
            for user in queryset:
                send_email_deactivate_notify(user, request)
            count = queryset.update(is_active=False)
            if count > 1:
                msg = "Selected " + str(count) + " Users have been disabled."
            else:
                msg = "Selected User has been disabled."
            messages.success(request, msg)
        except Exception:
            msg = "Fail to disable one or more Users"
            messages.error(request, msg)

    disable_user_notify.short_description = "Disable selected Users (will send notification email)"

    def disable_user(self, request, queryset):
        try:
            count = queryset.update(is_active=False)
            if count > 1:
                msg = "Selected " + str(count) + " Users have been disabled."
            else:
                msg = "Selected User has been disabled."
            messages.success(request, msg)
        except Exception:
            msg = "Fail to disable one or more Users"
            messages.error(request, msg)

    disable_user.short_description = "Disable selected Users (without sending notification email)"

    def email_verification(self, request, queryset):
        """
        sends a verification email to each selected unverified user
        """
        count = 0
        total = 0

        for user in queryset:

            user_id = user.id
            username = user.username

            # skip for already verified user or blocked user (active/blocked)
            if user.is_active and not user.is_blocked:
                continue

            try:
                send_email_verification(user, request)
                count = count + 1

            except (BadHeaderError, SMTPException):
                total = total + 1
                continue

        if count > 1:
            messages.success(
                request, "Verification email has been sent to " + str(count) + " unverified users.")
        elif count == 1:
            link = reverse("admin:sduser_sduser_change", args=[user_id])
            msg = format_html(
                "Verification email has been sent to User <a href='{}' target='_blank' rel='noopener'>{}</a>", link, username)
            messages.success(request, msg)
        else:
            if total > 1:
                msg = "The selected Users have already been verified."
            else:
                link = reverse("admin:sduser_sduser_change", args=[user_id])
                msg = format_html(
                    "The selected User <a href='{}' target='_blank' rel='noopener'>{}</a> has already been verified.", link, username)
            messages.error(request, msg)

    email_verification.short_description = "Send verification email (to unverified user)"

    # a field to keep track whether this user has activated the account (has reset the password upon log in)
    def activated(self, obj):
        if obj.is_superuser or obj.is_staff:
            return obj.default_pwd_updated
        else:
            return obj.is_active

    def save_model(self, request, obj, form, change):
        # need to make sure the pk is a required field when creating a new admin user
        # otherwise we need to check its existence for now
        if obj.pk:
            user = User.objects.get(pk=obj.pk)
            # Check first the case in which the password is not encoded, then check in the case that the password is encode
            if not (check_password(form.data['password'], user.password) or user.password == form.data['password']):
                obj.password = make_password(obj.password)
            else:
                obj.password = user.password
        else:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
    '''
    # No longer needed as I have nullify the confirmation field during clean_password on form saves
    # but keep the code here if at any point we want to modify the history directly...
    # (hack) filter out 'password2' by modifying the rendered content of template response
    def history_view(self, request, object_id, extra_context=None):
        #extra_context = extra_context or {}
        templateResponse = super().history_view(
            request, object_id, extra_context=extra_context,
        )
        if templateResponse is None:
            return 
        # this is needed for content but not rendered_content
        #templateResponse.render()

        # only passwrod2 changed => nothing else changed
        new_rendered_content = templateResponse.rendered_content.replace('Changed password2.', 'No fields changed.')
        # password2 is for validation only, not meaningful in history
        new_rendered_content = new_rendered_content.replace('password2', '')
        templateResponse.content = new_rendered_content

        return templateResponse
    '''


admin.site.register(User, UserAdmin)
