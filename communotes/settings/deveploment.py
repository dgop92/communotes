from datetime import timedelta
from decouple import config
from .base import *

DEBUG = True

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
}

DJOSER.update({
    'PASSWORD_RESET_CONFIRM_URL': "http://127.0.0.1:8000/password/reset/confirm/{uid}/{token}",
    'ACTIVATION_URL': "http://127.0.0.1:8000/activate/{uid}/{token}"
})

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')