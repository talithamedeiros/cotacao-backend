import logging
import raven

from .base import *

STATIC_ROOT = '/var/www/django/static'
MEDIA_ROOT = '/var/www/django/media'
DEBUG = False

ADMINS = (('', ''),)
MANAGERS = ADMINS

ALLOWED_HOSTS = []

# Session Settings
SESSION_COOKIE_AGE = 28800               # logout after 8 hours of inactivity
SESSION_SAVE_EVERY_REQUEST = True        # so, every "click" on the pages resets the expiry time
SESSION_EXPIRE_AT_BROWSER_CLOSE = True   # session cookie expires at close of browser

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{project_name}}',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': ''
    }
}

INTERNAL_IPS = ('127.0.0.1')
INSTALLED_APPS += ['gunicorn', 'raven.contrib.django.raven_compat',]

SENTRY_DSN = ''
SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                    '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}

SENTRY_CELERY_LOGLEVEL = logging.INFO
RAVEN_CONFIG = {
    'CELERY_LOGLEVEL': logging.INFO,
    'DSN': SENTRY_DSN
}
