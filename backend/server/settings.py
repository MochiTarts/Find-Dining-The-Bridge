"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

# Custom URL for Django views to redirect requests to Angular Routing
VIEW_REDIRECT_URL = os.environ.get('VIEW_REDIRECT_URL')

if DEBUG:
    VIEW_REDIRECT_URL = 'http://localhost:4200'


# Application definition

INSTALLED_APPS = [
    'server', # This is added for my admin.py to take effect first (which replaces admin site with my custom one)
    #'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sduser',
    'index',
    'rest_framework',
    'corsheaders',
    'gmailapi_backend',
    'login_audit',
    'snowpenguin.django.recaptcha2',
    'subscriber_profile',
    'restaurant_owner',
    'restaurant',
    'ckeditor',
    'article',
    'image',
    
    #'user.apps.SDUserConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    #'spa.middleware.SPAMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # this should be above common middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'HOST': 'mongodb-test',
        'PORT': 27117,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {   
        'NAME': 'utils.validators.UserPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Override default user model
AUTH_USER_MODEL = 'sduser.SDUser'

# Override default auth backend
AUTHENTICATION_BACKENDS = ['sduser.backends.EmailBackend']

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '100/hour'
    },
    'EXCEPTION_HANDLER': 'utils.exception_handler.views_exception_handler'
}
# doesn't work right now because Djongo can't translate aggregation functions in sql



'''
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=365),
    'JWT_PAYLOAD_HANDLER': 'sduser.backends.jwt_payload_handler',
}
'''

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = os.environ.get('SSL_REDIRECT') == 'True'

if os.environ.get('ALLOWED_HOSTS') != None:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')

if os.environ.get('CORS_ALLOWED') != None:
    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED').split(',')

CORS_ALLOW_METHODS = (
'GET',
'POST',
'PUT',
'PATCH',
'DELETE',
'OPTIONS'
 )

CSRF_TRUSTED_ORIGINS = [
    #"http://localhost:4200",
    #"http://127.0.0.1:4200",
    ".finddining.ca",
]

MAIN_SITE_URL = os.environ.get('MAIN_SITE_URL')

#CSRF_COOKIE_NAME = 'XSRF-TOKEN'
#CSRF_HEADER_NAME = 'HTTP_X_XSRF_TOKEN'

CORS_ALLOW_CREDENTIALS = True
#CSRF_COOKIE_DOMAIN = ".localhost"
SESSION_COOKIE_SAMESITE = None

EMAIL_BACKEND = 'gmailapi_backend.mail.GmailBackend'

GMAIL_API_CLIENT_ID = os.environ.get('GMAIL_API_CLIENT_ID')
GMAIL_API_CLIENT_SECRET = os.environ.get('GMAIL_API_CLIENT_SECRET')
GMAIL_API_REFRESH_TOKEN = os.environ.get('GMAIL_API_REFRESH_TOKEN')


JWT_ALGORITHM = 'HS256'

# JWT settings
SIMPLE_JWT = {
    # for testing
    #'ACCESS_TOKEN_LIFETIME': timedelta(seconds=10),
    #'REFRESH_TOKEN_LIFETIME': timedelta(seconds=60),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': JWT_ALGORITHM,
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    # sliding tokens are not being used
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = ''
import sys
# not exhaustive, we simply need to add any manage.py command that we would run and not setting static root when running them
#or sys.argv[1] not in ['runserver', 'makemigrations', 'migrate', 'createsuperuser', ...]
if len(sys.argv) < 2 or sys.argv[1] not in ['runserver', 'makemigrations', 'migrate', 'createsuperuser', 'collectstatic']:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]


#SESSION_COOKIE_DOMAIN = '.localhost'

# for development only, this is a “dummy” cache that doesn’t actually cache
# it just implements the cache interface without doing anything
'''
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
'''
# cache in db
'''
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}
'''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'django_cache',
    }
}


GOOGLE_OAUTH2_CLIENT_ID=os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')

# reCaptcha v2 for admin portal (still need to add the ip on recaptcha settings)
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAP_PRIV_KEY')
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAP_PUB_KEY')

GEOCODE_API_KEY = os.environ.get('GEOCODE_API_KEY')

GA_VIEW_ID = os.environ.get('GA_VIEW_ID')

GOOGLE_OAUTH2_CLIENT_EMAIL = os.environ.get('GOOGLE_OAUTH2_CLIENT_EMAIL')
# note that the replace is required after reading
GOOGLE_OAUTH2_PRIVATE_KEY = os.environ.get('GOOGLE_OAUTH2_PRIVATE_KEY').replace('\\n', '\n')

GOOGLE_ANALYTICS_CLIENT_EMAIL = os.environ.get('GOOGLE_ANALYTICS_CLIENT_EMAIL')
# note that the replace is required after reading
GOOGLE_ANALYTICS_PRIVATE_KEY = os.environ.get('GOOGLE_ANALYTICS_PRIVATE_KEY').replace('\\n', '\n')