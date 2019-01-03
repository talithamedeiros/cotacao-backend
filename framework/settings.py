#-*- coding: utf-8 -*-


##################################################
#               DJANGO IMPORTS                   #
##################################################
import os
import sys
from os.path import abspath, basename, dirname, join, normpath
##################################################


'''
    PROJECT DIRS
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(normpath(join(BASE_DIR, 'apps')))

'''
    PROJECT SECRET KEY
'''
SECRET_KEY = 'od1hqq3a^k5qidbity73r!f-_@6*apiif0ni#ni_x$qjwxrock'

'''
    PROJECT DATA FORMAT
'''
DATE_INPUT_FORMATS = ('%d-%m-%Y')

'''
    SET TRUE TO ENABLE DEBUG
'''
DEBUG = True

'''
    SET ADMINS TO ENABLE DEBUG
'''
ADMINS = (
    ('Ylgner', 'ylgner.becton@gmail.com'),
)
SITE_NAME=''
MANAGERS = ADMINS

'''
    PROJECT HOSTS
'''
ALLOWED_HOSTS = ['localhost']

'''
    CUSTOM AUTH
'''
AUTH_USER_MODEL = 'default.Usuario'


'''
    APLICATIONS
'''
DJANGO_APPS = [
    'material',
    'material.frontend',
    'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'smuggler',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'rest_auth',
    'oauth2_provider',
    'rest_auth.registration',
    'debug_toolbar.apps.DebugToolbarConfig',
]

CUSTOM_APPS = [
    'apps.default', 
    # SUBCLASS APPS
    'apps.api_rest',
]

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS


'''
    MIDDLEWARES
'''
DJANGO_MIDDLEWARES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CUSTOM_MIDDLEWARES = [

]

MIDDLEWARE_CLASSES = DJANGO_MIDDLEWARES + CUSTOM_MIDDLEWARES


'''
    DJANGO CORS
'''
CORS_ORIGIN_ALLOW_ALL = True 


'''
    LOGIN
'''
LOGIN_REDIRECT_URL = '/perfil'
LOGIN_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = None
SOCIALACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'user_birthday' ,'publish_actions','user_friends'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
  }
}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_REQUIRED = False


'''
    URLS
'''
ROOT_URLCONF = 'framework.urls'



'''
    TEMPLATES
'''
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            'templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                "django.template.context_processors.i18n",
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


'''
    WSGI
'''
WSGI_APPLICATION = 'framework.wsgi.application'



'''
    DATABASES
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


'''
    AUTHENTICATION
'''
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
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


'''
    INTERNACIONALIZATION
'''
LANGUAGE_CODE = 'pt-br'
LANGUAGES = (
 ('pt-br', ('Brasilian Portuguese')),
 ('en', ('English')),
 ('es', ('Spanish')),
)
LOCALE_PATHS = (
   os.path.join(BASE_DIR, 'locale'),
)
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 2
THUMBNAIL_DEBUG = True

'''
    STATIC FILES
'''
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

'''
    UPLOADS MEDIA
'''
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

'''
    LOG CONFIG
'''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


'''
    EMAIL
'''
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '#'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


'''
    IUGU
'''
IUGU_TOKEN = '#'


'''
    SMS_TOKEN = 
'''
SMS_TOKEN = '#'


'''
    REST FRAMEWORK
'''
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
}


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
          "type": "apiKey",
          "name": "Authorization",
          "in": "header"
        }
    },
    'LOGIN_URL':'rest_framework:login',
    'LOGOUT_URL':'rest_framework:logout',
}


API_URL = "http://127.0.0.1:8000/o/token/"

CHECK_SMS = True
"""
    DJANGO_FILER
"""

INSTALLED_APPS += [
    'easy_thumbnails',
    'filer',
    'mptt',
]

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
FILER_CANONICAL_URL = 'sharing/'
