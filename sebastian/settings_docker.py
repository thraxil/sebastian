# flake8: noqa
import os
import os.path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .settings_shared import INSTALLED_APPS, MIDDLEWARE, STATIC_ROOT

from .settings_shared import *  # isort:skip


app = "sebastian"


# required settings:
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# optional/defaulted settings
DB_NAME = os.environ.get("DB_NAME", app)
DB_HOST = os.environ.get(
    "DB_HOST", os.environ.get("POSTGRESQL_PORT_5432_TCP_ADDR", "")
)
DB_PORT = int(
    os.environ.get(
        "DB_PORT", os.environ.get("POSTGRESQL_PORT_54342_TCP_PORT", 5432)
    )
)
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

if "ALLOWED_HOSTS" in os.environ:
    ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

TIME_ZONE = os.environ.get("TIME_ZONE", "America/New_York")

EMAIL_HOST = os.environ.get(
    "EMAIL_HOST", os.environ.get("POSTFIX_PORT_25_TCP_ADDR", "localhost")
)
EMAIL_PORT = os.environ.get(
    "EMAIL_PORT", os.environ.get("POSTFIX_PORT_25_TCP_PORT", 25)
)

SERVER_EMAIL = os.environ.get("SERVER_EMAIL", app + "@thraxil.org")

# -------------------------------------------

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DB_NAME,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
}

SENTRY_DSN: str = os.getenv("RAVEN_DSN", "")
if SENTRY_DSN != "":
    ENVIRONMENT = "production"
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(
                middleware_spans=False,
                signals_spans=False,
                cache_spans=False,
            )
        ],
        traces_sample_rate=1.0,
        send_default_pii=False,
        environment=ENVIRONMENT,
    )

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
