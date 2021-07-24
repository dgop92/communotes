from datetime import timedelta
import dj_database_url
from .base import *
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', cast=Csv())

MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
MIDDLEWARE.insert(2, 'whitenoise.middleware.WhiteNoiseMiddleware')

db_from_env = dj_database_url.config(conn_max_age=600)

DATABASES = {
    'default': db_from_env
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
}

DJOSER['PASSWORD_RESET_CONFIRM_URL'] = "http://127.0.0.1:8000/password/reset/confirm/{uid}/{token}" 
DJOSER['ACTIVATION_URL'] = "http://127.0.0.1:8000/activate/{uid}/{token}",

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = True

BASE_INSTALLED_APPS.extend(['cloudinary_storage', 'cloudinary',])

MEDIA_URL = '/communotes/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
