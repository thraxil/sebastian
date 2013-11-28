# flake8: noqa
from settings import *
import os.path

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_NAME = 'sebastian'

TEMPLATE_DIRS = (
    "/var/www/sebastian/sebastian/sebastian/leitner/templates",
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/sebastian/uploads/media/data/'

SERVER_EMAIL = 'anders@columbia.edu'

STATICFILES_DIRS = ()
STATIC_ROOT = "/var/www/sebastian/sebastian/media/"

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
