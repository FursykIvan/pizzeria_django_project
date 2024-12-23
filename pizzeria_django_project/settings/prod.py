from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
 'default': {
   'ENGINE': 'django.db.backends.postgresql',
   'NAME': os.getenv('POSTGRES_DB'),
   'USER': os.getenv('POSTGRES_USER'),
   'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
   'HOST': os.getenv('POSTGRES_HOST'),
   'PORT': os.getenv('POSTGRES_DB_PORT', 5432),
   'OPTIONS': {
     'sslmode': 'require',
   },
 }
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
