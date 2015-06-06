"""
Base settings for Cards Project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
import sys

DJANGO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

SITE_ROOT = os.path.dirname(DJANGO_ROOT)

SITE_NAME = os.path.basename(DJANGO_ROOT)

sys.path.append(DJANGO_ROOT)


# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

SECRET_KEY = r"q4$#tnadep*^j6f1240=%3s6tw7cpq%i)if=yg)7qe&eug3de5"

DEBUG = True


TEMPLATE_DIRS = (os.path.join(DJANGO_ROOT, "templates"),)

TEMPLATE_DEBUG = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


# Application definition

ALLOWED_HOSTS = []

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOCAL_APPS = (
    'pipeline',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cards.urls'

WSGI_APPLICATION = 'cards.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DJANGO_ROOT, 'db.sqlite3'),
    }
}

FIXTURE_DIRS = (
    os.path.join(SITE_ROOT, 'fixtures'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(DJANGO_ROOT, 'static')
STATICFILES_DIRS = (
    os.path.join(DJANGO_ROOT, 'assets'),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE_CSS = {
    'libraries': {
        'source_filenames':
            ('bower_components/bootstrap/dist/css/bootstrap.css',),
        'output_filename': 'css/libs.min.css',
    },
    'custom': {
        'source_filenames':
             ('css/cards.css',),
        'output_filename': 'css/custom.min.css',
    }
}

PIPELINE_JS = {
    'libraries': {
        'source_filenames':
            ('bower_components/jquery/dist/jquery.js',),
        'output_filename': 'js/libs.min.js',
    }
}
