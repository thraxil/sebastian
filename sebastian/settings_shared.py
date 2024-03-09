# flake8: noqa
import os.path

from thraxilsettings.shared import common

app = "sebastian"
base = os.path.dirname(__file__)
locals().update(common(app=app, base=base))

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
            os.path.join(os.path.dirname(__file__), "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
CSRF_TRUSTED_ORIGINS = ["https://cards.thraxil.org"]

STATIC_ROOT = ""

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "waffle.middleware.WaffleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

try:
    from local_settings import *
except ImportError:
    pass
