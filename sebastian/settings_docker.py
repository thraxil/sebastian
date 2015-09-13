# flake8: noqa
from settings_shared import *
from thraxilsettings.docker import common
import os.path

app = 'sebastian'
base = os.path.dirname(__file__)

locals().update(
    common(
        app=app,
        base=base,
        celery=False,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
    ))
