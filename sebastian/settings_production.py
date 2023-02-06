# flake8: noqa
import os.path

from .settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_NAME = "sebastian"

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), "leitner/templates"),)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = "/var/www/sebastian/uploads/media/data/"

SERVER_EMAIL = "anders@columbia.edu"

STATICFILES_DIRS = ()
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../media")

COMPRESS_OFFLINE = True

AWS_S3_CUSTOM_DOMAIN = "d1txj5n8ebgwx3.cloudfront.net"
AWS_IS_GZIPPED = True

AWS_STORAGE_BUCKET_NAME = "thraxil-sebastian-static-prod"
AWS_PRELOAD_METADATA = True
DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
STATICFILES_STORAGE = "cacheds3storage.MediaRootS3BotoStorage"
S3_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
DEFAULT_FILE_STORAGE = "cacheds3storage.MediaRootS3BotoStorage"
MEDIA_URL = S3_URL + "/media/"
COMPRESS_STORAGE = "cacheds3storage.CompressorS3BotoStorage"
AWS_QUERYSTRING_AUTH = False


if "migrate" not in sys.argv:
    INSTALLED_APPS = INSTALLED_APPS + [
        "raven.contrib.django.raven_compat",
    ]


# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
