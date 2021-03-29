from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from sduser.utils import send_email_verification


User = get_user_model()

# an instance is used for the second param of send_verification_email function
class SDUserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role',)


class AdminForm(ModelForm):
    # note that modification to this field will show up in the history (right now I am explicitly filtering it out in history_view)
    password2 = forms.CharField(
        label=_("password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
        required=False,
        help_text=_(
            "If you are changing the password, enter the same password as before, for verification.")
    )

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_missing': _("Please confirm your password"),
    }

    def __init__(self, *args, **kwargs):
        #password = self.fields.get('password2')
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'first_name', 'last_name', 'email',
                  'role', 'auth_id', 'refresh_token', 'is_blocked', 'is_superuser', 
                  'is_staff', 'is_active', 'groups', 'user_permissions')
        #exclude = ['last_login', 'date_joined']
        # change the password input from char field to pwd field (with placeholders)
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }
        pwd_help_text = '<ul><li>Password is not stored in plain text but hashed.</li><li>If you are modifying this field (during creation or reset), follow the rules below. Once you save it, this field will be hashed.</li></ul>'

        help_texts = {
            'password': format_html(pwd_help_text) + format_html(password_validation.password_validators_help_text_html())
        }
    
    def save(self, commit=True):
        user = super(AdminForm, self).save(commit=False)

        # only send email verification when user is not active (yet) and have never logged in before (no refresh token, password has not been hashed)
        if not user.is_active and user.refresh_token is None and not user.password.startswith('pbkdf2_sha256'):
            try:
                send_email_verification(user=user, site=admin.site.site_url)
            except Exception:
                print('fail to send email verification to ' + user.username + ' (' + user.email + ')')
        if commit:
            user.save()

        return user

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # confirmation field
        # this is obtained from data instead of cleaned data because there is no corresponding method for it when clean is called
        password2 = self.data.get('password2')

        # value is not hashed -> either during creation or resetting password
        if not password.startswith('pbkdf2_sha256'):
            password_validation.validate_password(password)
            if password and password2:
                # password confirmation failed
                if password != password2:
                    raise forms.ValidationError(
                        self.error_messages['password_mismatch'],
                        code='password_mismatch',
                    )
                # password confirmed
                else:
                    # reset pwd2 because there is no need to store the confirmation field
                    self.data = self.data.copy()
                    self.data['password2'] = None
            # password changed but didn't confirm
            if not password2:
                raise forms.ValidationError(
                    self.error_messages['password_missing'],
                    code='password_missing',
                )
        else:
            # reset pwd2 because there is no need to store the confirmation field
            self.data = self.data.copy()
            self.data['password2'] = None

        return self.cleaned_data["password"]


# note that subclassing AdminPasswordChangeForm will not work...
class SDPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password0 = self.cleaned_data.get('old_password')
        password1 = self.cleaned_data.get('new_password1')
        #logger.info(password0)
        #logger.info(password1)
        if password0 and password1:
            if password0 == password1:
                raise forms.ValidationError("You may not use the same old password!",code='password_incorrect')
        return password1


class SDPasswordResetForm(PasswordResetForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    class Meta:
        fields = ('email', 'captcha')