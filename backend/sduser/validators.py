from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError

def validate_signup_user(user):
    invalid = []
    if not validate_email_address(user['email']):
        invalid.append('email')

    if not validate_username(user['username']):
        invalid.append('username')

    return invalid


# name should not contain number or symbols
def validate_name(name):
    try:
        regexValidator = RegexValidator('^[^±!@£$%^&*_+§¡€#¢§¶•ªº«\\/<>?:;|=.,0-9]{1,40}$')
        regexValidator(name)
        return True
    except ValidationError:
        return False

# username should not contain weird symbols (@, +, -, _, and . are allowed)
def validate_username(name):
    try:
        regexValidator = RegexValidator('^[^±!£$%^&*§¡€#¢§¶•ªº«\\/<>?:;|=,]{1,100}$')
        regexValidator(name)
        return True
    except ValidationError:
        return False

def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False