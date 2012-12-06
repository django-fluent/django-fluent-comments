# Django settings for example project.
from os.path import join, dirname, realpath

# Add parent path,
# Allow starting the app without installing the module.
import sys
sys.path.insert(0, dirname(dirname(realpath(__file__))))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': dirname(__file__) + '/demo.db',
    }
}

TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = join(dirname(__file__), "media")
MEDIA_URL = '/media/'
STATIC_ROOT = join(dirname(__file__), "static")
STATIC_URL = '/static/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-#@bi6bue%#1j)6+4b&#i0g-*xro@%f@_#zwv=2-g_@n3n_kj5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    join(dirname(__file__), "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Example app
    'article',
    'theme1',

    # Required modules
    'crispy_forms',
    'fluent_comments',
    'django.contrib.comments',  # below theme1 and fluent_comments
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# fluent-comments settings:
FLUENT_COMMENTS_USE_EMAIL_MODERATION = True
FLUENT_COMMENTS_MODERATE_AFTER_DAYS = 14
FLUENT_COMMENTS_CLOSE_AFTER_DAYS = 60
FLUENT_COMMENTS_AKISMET_ACTION = 'moderate'
AKISMET_API_KEY = None  # Add your Akismet key here to enable Akismet support
AKISMET_IS_TEST = True  # for development/example apps.
