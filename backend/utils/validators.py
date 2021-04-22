from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator, RegexValidator
#from django.core import validators
from better_profanity import profanity
from collections import Iterable

def check_script_injections(value):
    if isinstance(value, Iterable) and type(value) != str:
        for val in value:
            check_script_injection(val)
    else:
        check_script_injection(value)


def check_script_injection(value):
    if value is not None:
        val = ''
        try:
            if type(value) == str:
                val = value
            else:
                val = str(value)
        except Exception as e:
            pass
        finally:
            if val.find('<script>') != -1:
                raise ValidationError(_('Field should not contain scripts!'))
                #raise ValidationError(_('Script injection in %(value)s'),params={'value': val})


# validate url that may or maynot contain a shema
def validate_url(website):
    try:
        urlValidator = URLValidator()
        scheme = website.split('://')[0].lower()
        if scheme not in ['http', 'https', 'ftp', 'ftps']:
            urlValidator('https://' + website)
        else:
            urlValidator(website)
    except ValidationError as e:
        raise e

# name should not contain weird symbols


def validate_name(name):
    try:
        regexValidator = RegexValidator(
            '^[^±!@£$%^&*_+§¡€#¢§¶•ªº«\\/<>?:;|=.,0-9]{1,40}$')
        regexValidator(name)
    except ValidationError as e:
        raise e

# postal code should be A1A 1A1 or A1A-1A1 or A1A1A1


def validate_postal_code(code):
    try:
        regexValidator = RegexValidator(
            '^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$')
        regexValidator(code)
    except ValidationError as e:
        raise e


def validate_profane_content(content):
    """ Validates text for any profanity

    :param content: text content to be validated
    :type content: str
    :raises: ValidationError upon detecting profane word(s) in content
    :return: None
    :rtype: None
    """
    with open('utils/more_profanity.txt', 'r') as f:
        additional_words = [line.strip() for line in f]

    profanity.add_censor_words(additional_words)
    if profanity.contains_profanity(content):
        raise ValidationError("Content contains profane language")


class UserPasswordValidator():

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"

        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d digit.') % {
                                  'min_length': self.min_length}, code='password_too_simple',)
        if not validate_mix_case(password):
            raise ValidationError(_('Password must contain at least %(min_length)d uppercase and %(mind_length)d lowercase letter.') % {
                                  'min_length': self.min_length}, code='password_too_simple',)
        if not any(char in special_characters for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d special character.') % {
                                  'min_length': self.min_length}, code='password_too_simple',)

    def get_help_text(self):
        return "Password must contain a special character, an uppercase letter, and a lowercase letter"


def validate_mix_case(string):
    letters = set(string)
    mixed = any(letter.islower() for letter in letters) and any(
        letter.isupper() for letter in letters)
    return mixed
