# flake8: noqa
import os.path

from thraxilsettings.shared import common

app = "sebastian"
base = os.path.dirname(__file__)
locals().update(common(app=app, base=base))

INSTALLED_APPS += [  # noqa
    "sebastian.leitner",
]

ALLOWED_HOSTS += ["cards.thraxil.org"]  # noqa

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

try:
    from local_settings import *
except ImportError:
    pass
