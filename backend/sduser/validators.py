from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from utils.validators import check_script_injection

def validate_signup_user(user):
    invalid = []
    if not validate_email_address(user['email']):
        invalid.append('email')

    if not validate_username(user['username']):
        invalid.append('username (should not contain spaces or spacial characters)')
    
    try:
        check_script_injection(user['username'])
    except ValidationError as e:
            invalid.append('username (should not contain scripts)')

    try:
        check_script_injection(user['password'])
        # validate password against auth AUTH_PASSWORD_VALIDATORS
        validate_password(user['password'])
    except ValidationError:
        invalid.append('password (contain scripts or does not meet complexity requirements)')

    return invalid


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
