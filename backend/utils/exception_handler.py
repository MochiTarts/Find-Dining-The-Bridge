from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail
from django.http import JsonResponse

from django.core.exceptions import MultipleObjectsReturned, ValidationError, ObjectDoesNotExist
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, MethodNotAllowed, ParseError
from rest_framework_simplejwt.exceptions import AuthenticationFailed 
from django.db import IntegrityError

import jsonschema, json

def views_exception_handler(exc, context):
    """ Custom handler for standardizing exceptions that will be thrown from the API views """
    response = exception_handler(exc, context)

    status_400_exceptions = (
        jsonschema.exceptions.ValidationError, json.decoder.JSONDecodeError, IntegrityError,
        MultipleObjectsReturned, ValidationError, ParseError, ObjectDoesNotExist
    )
    status_401_excpetions = (NotAuthenticated, AuthenticationFailed)
    status_403_exceptions = (PermissionDenied)
    status_404_exceptions = (NotFound)
    status_405_exceptions = (MethodNotAllowed)
    status_500_exceptions = (ValueError)

    # checks if the exception is part of the status 400 exceptions tuple
    if isinstance(exc, status_400_exceptions):
        if hasattr(exc, 'message'):
            detail = exc.message
        elif hasattr(exc, 'message_dict'):
            detail = exc.message_dict
        else:
            detail = str(exc)

        if hasattr(exc, 'code'):
            code = exc.code
        else:
            code = "bad_request"
        custom_error_response = {
            "status": 400,
            "code": code,
            "detail": detail
        }
        return JsonResponse(custom_error_response, status=400)

    # 401 are all DRF exceptions so we can simply use its response handling
    if isinstance(exc, status_401_excpetions):
        if response is not None:
            response.data['status'] = response.status_code
        return response

    if isinstance(exc, status_403_exceptions):
        if hasattr(exc, 'message'):
            detail = exc.message
        elif hasattr(exc, 'message_dict'):
            detail = exc.message_dict
        else:
            detail = str(exc)

        if hasattr(exc, 'code'):
            code = exc.code
        else:
            code = "forbidden"
        custom_error_response = {
            "status": 403,
            "code": code,
            "detail": detail
        }
        return JsonResponse(custom_error_response, status=403)

    if isinstance(exc, status_404_exceptions):
        if hasattr(exc, 'message'):
            detail = exc.message
        elif hasattr(exc, 'message_dict'):
            detail = exc.message_dict
        else:
            detail = str(exc)

        if hasattr(exc, 'code'):
            code = exc.code
        else:
            code = "not_found"
        custom_error_response = {
            "status": 404,
            "code": code,
            "detail": detail
        }
        return JsonResponse(custom_error_response, status=404)

    if isinstance(exc, status_405_exceptions):
        if hasattr(exc, 'message'):
            detail = exc.message
        elif hasattr(exc, 'message_dict'):
            detail = exc.message_dict
        else:
            detail = str(exc)

        if hasattr(exc, 'code'):
            code = exc.code
        else:
            code = "method_not_allowed"
        custom_error_response = {
            "status": 405,
            "code": code,
            "detail": detail
        }
        return JsonResponse(custom_error_response, status=405)

    if isinstance(exc, status_500_exceptions):
        if hasattr(exc, 'message'):
            detail = exc.message
        elif hasattr(exc, 'message_dict'):
            detail = exc.message_dict
        else:
            detail = str(exc)

        if hasattr(exc, 'code'):
            code = exc.code
        else:
            code = "internal_server_error"
        custom_error_response = {
            "status": 500,
            "code": code,
            "detail": detail
        }
        return JsonResponse(custom_error_response, status=500)

    # Returns None if any other exception occured. Meant for debugging and fixing issues
    return response