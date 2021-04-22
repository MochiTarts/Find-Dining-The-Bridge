
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(AuthenticationForm):
    '''
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
    '''

    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    class Meta:
        model = User
        fields = ('username', 'password', 'captcha')
