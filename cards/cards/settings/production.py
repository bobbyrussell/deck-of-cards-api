"""
Production settings for the Cards Project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from .base import *

# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

DEBUG = False


# Application definition

ALLOWED_HOSTS = []

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
