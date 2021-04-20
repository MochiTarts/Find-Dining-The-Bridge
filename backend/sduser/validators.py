from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


def validate_signup_user(user):
    invalid = []
    if not validate_email_address(user['email']):
        invalid.append('email')

    if not validate_username(user['username']):
        invalid.append('username')

    try:
        # validate password against auth AUTH_PASSWORD_VALIDATORS
        validate_password(user['password'])
    except ValidationError:
        invalid.append('password')

    return invalid


# name should not contain number or symbols
def validate_name(name):
    try:
        regexValidator = RegexValidator(
            '^[^±!@£$%^&*_+§¡€#¢§¶•ªº«\\/<>?:;|=.,0-9]{1,40}$')
        regexValidator(name)
        return True
    except ValidationError:
        return False

# username should not contain weird symbols (@, +, -, _, and . are allowed)


def validate_username(name):
    try:
        regexValidator = RegexValidator(
            #'^[^±!£$%^&*§¡€#¢§¶•ªº«\\/<>?:;|=,]{1,150}$')
            '^[^±£$§¡€¢§¶•ªº«]{1,150}$')
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
