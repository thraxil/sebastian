import os.path
import sys
from pathlib import Path

app = "sebastian"
base = Path(__file__).resolve().parent.parent

DEBUG = True

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": app,
        "HOST": "",
        "PORT": 5432,
        "USER": "",
        "PASSWORD": "",
        "ATOMIC_REQUESTS": True,
    }
}

if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
            "HOST": "",
            "PORT": "",
            "USER": "",
            "PASSWORD": "",
            "ATOMIC_REQUESTS": True,
        }
    }

TEST_RUNNER = "django.test.runner.DiscoverRunner"

TIME_ZONE = "America/New_York"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/" + app + "/uploads/"
MEDIA_URL = "/uploads/"
SECRET_KEY = "you must override this"  # nosec

ROOT_URLCONF = app + ".urls"

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(base, "static"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

INTERNAL_IPS = ["127.0.0.1"]
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[" + app + "] "
EMAIL_HOST = "localhost"
SERVER_EMAIL = app + "@thraxil.org"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 265 * 5

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
}


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "debug_toolbar",
    "waffle",
    "smoketest",
    "gunicorn",
    "sebastian.leitner",
]

ALLOWED_HOSTS = ["localhost", "cards.thraxil.org"]

USE_TZ = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(base, "sebastian/templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
CSRF_TRUSTED_ORIGINS = ["https://cards.thraxil.org"]

STATIC_ROOT = os.path.join(base, "staticfiles")

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "waffle.middleware.WaffleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
