from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from collections import Iterable
from django.core.validators import URLValidator, RegexValidator
from profanityfilter import ProfanityFilter
#from django.core import validators

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
        regexValidator = RegexValidator('^[^±!@£$%^&*_+§¡€#¢§¶•ªº«\\/<>?:;|=.,0-9]{1,40}$')
        regexValidator(name)
    except ValidationError as e:
        raise e

# postal code should be A1A 1A1 or A1A-1A1 or A1A1A1
def validate_postal_code(code):
    try:
        regexValidator = RegexValidator('^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$')
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
    print(ProfanityFilter().is_clean(content))
    if not ProfanityFilter().is_clean(content):
        raise ValidationError("Content contains profane language")