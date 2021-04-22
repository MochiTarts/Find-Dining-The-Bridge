from django.conf import settings

def environment_var(request):

    ENVIRONMENT_NAME = "Development Server"
    ENVIRONMENT_COLOR ="Grey"

    if settings.MAIN_SITE_URL:
        URL = settings.MAIN_SITE_URL
        if 'test' in URL:
            ENVIRONMENT_NAME = "Test Server"
            ENVIRONMENT_COLOR = "Yellow"
        elif 'uat' in URL:
            ENVIRONMENT_NAME = "UAT Server"
            ENVIRONMENT_COLOR = "Orange"
        else:
            ENVIRONMENT_NAME = "Production Server"
            ENVIRONMENT_COLOR = "Red"

    return {
        'ENVIRONMENT_NAME': ENVIRONMENT_NAME,
        'ENVIRONMENT_COLOR': ENVIRONMENT_COLOR,
    }