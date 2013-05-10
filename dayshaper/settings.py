""" dayshaper.settings

    This module defines the various settings for the Dayshaper project.
"""
import os.path
import sys

#############################################################################

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

#############################################################################

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = None

MANAGERS = ADMINS

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

TIME_ZONE = None

USE_TZ = False

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = ''

STATIC_URL = '/assets/'

STATICFILES_DIRS = (
    (os.path.join(ROOT_DIR, "dayshaper", "assets")),
)

SERVE_STATIC_MEDIA = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'q%_+l@fnlzvqcwou+223r*g79$l%ke*20xnswi5qh+ro4h_sey'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dayshaper.urls'

WSGI_APPLICATION = 'dayshaper.wsgi.application'

TEMPLATE_DIRS = (
  os.path.dirname(__file__),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Enable the "south" database migration toolkit.

    'south',

    # Install our various Dayshaper apps.

    'dayshaper.shared',
    'dayshaper.web',
)

# Set up our database.

if 'test' in sys.argv:
    # Use SQLite for unit tests.
    DATABASES = {'default' : {'ENGINE' : "django.db.backends.sqlite3"}}
else:
    DATABASES = {
        'default': {
            'ENGINE'   : 'django.db.backends.postgresql_psycopg2',
            'NAME'     : 'dayshaper',
            'USER'     : 'postgres',
            'PASSWORD' : 'hal9000',
            'HOST'     : '',
            'PORT'     : '',
        }
    }

