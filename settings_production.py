from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_NAME = 'sebastian'

TEMPLATE_DIRS = (
    "/var/www/sebastian/leitner/templates",
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/sebastian/media/'

SERVER_EMAIL = 'anders@columbia.edu'
