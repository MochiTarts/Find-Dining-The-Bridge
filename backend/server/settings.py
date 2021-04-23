"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import sys
import os
import datetime
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Used for automatically setting user registered with this email an admin on signup
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

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


ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # This is added for my admin.py to take effect first (which replaces admin site with my custom one)
    'server',
    # 'whitenoise.runserver_nostatic',
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
    'django.contrib.admindocs',
    'drf_yasg',
    'newsletter',

    # 'user.apps.SDUserConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'spa.middleware.SPAMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # this should be above common middleware
    'corsheaders.middleware.CorsMiddleware',
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
                'utils.context_processors.environment_var'
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
        'HOST': os.environ.get('DB_HOST'),
        'TEST': {
            'NAME': 'scdining-unit-tests'
        }
        # 'USER': os.environ.get('DB_USER'),
        # 'PASSWORD': os.environ.get('DB_PASS')
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
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
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
        'anon': '121/minute',
        'user': '201/minute'
    },
    'EXCEPTION_HANDLER': 'utils.exception_handler.views_exception_handler',
}
# doesn't work right now because Djongo can't translate aggregation functions in sql

SWAGGER_SETTINGS = {
    'SUPPORTED_SUBMIT_METHODS': [],
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': None,
}

'''
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=365),
    'JWT_PAYLOAD_HANDLER': 'sduser.backends.jwt_payload_handler',
}
'''
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
if not DEBUG:
    # Once you confirm that all assets are served securely on your site (i.e. HSTS didn’t break anything),
    # it’s a good idea to increase this value so that infrequent visitors will be protected
    # (31536000 seconds, i.e. 1 year, is common).
    SECURE_HSTS_SECONDS = 3600
    # set this to false to allow subdomain with invalid SSL for testing
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# the browser will only load the resource in a frame
# if the request originated from the same site
X_FRAME_OPTIONS = 'SAMEORIGIN'

# To prevent the browser from guessing the content type
# and force it to always use the type provided in the Content-Type header
# Need to also set this in the front-end Web server if it is the one serving
# user uploaded files
SECURE_CONTENT_TYPE_NOSNIFF = True

# To enable the XSS filter in the browser
# and force it to always block suspected XSS attacks
SECURE_BROWSER_XSS_FILTER = True

SECURE_SSL_REDIRECT = os.environ.get('SSL_REDIRECT') == 'True'

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

CORS_ALLOWED_ORIGINS = [
    "https://localhost:4200",
    "http://127.0.0.1:4200",
    "https://jsonip.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
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
    # 'ACCESS_TOKEN_LIFETIME': timedelta(seconds=10),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(seconds=60),
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
# set staticfiles_dirs for django templates to render static files on development server
if len(sys.argv) > 2 and sys.argv[1] == 'runserver':
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static/"),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")


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
# cache in db (doesn't work with current version of djongo and sqlparser mainly because it is not compatible with aggregate functions)
'''
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}
'''
# resort to use file cache as it doesn't require translation of aggregate functions from SQL to NoSQL
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'django_cache',
    }
}


GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')

# reCaptcha v2 for admin portal (still need to add the ip on recaptcha settings)
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAP_PRIV_KEY')
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAP_PUB_KEY')

GEOCODE_API_KEY = os.environ.get('GEOCODE_API_KEY')

GA_VIEW_ID = os.environ.get('GA_VIEW_ID')

GOOGLE_OAUTH2_CLIENT_EMAIL = os.environ.get('GOOGLE_OAUTH2_CLIENT_EMAIL')
# note that the replace is required after reading
GOOGLE_OAUTH2_PRIVATE_KEY = os.environ.get(
    'GOOGLE_OAUTH2_PRIVATE_KEY').replace('\\n', '\n')

GOOGLE_ANALYTICS_CLIENT_EMAIL = os.environ.get('GOOGLE_ANALYTICS_CLIENT_EMAIL')
# note that the replace is required after reading
GOOGLE_ANALYTICS_PRIVATE_KEY = os.environ.get(
    'GOOGLE_ANALYTICS_PRIVATE_KEY').replace('\\n', '\n')
