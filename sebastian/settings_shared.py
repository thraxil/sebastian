# flake8: noqa
import os.path
from thraxilsettings.shared import common

app = 'sebastian'
base = os.path.dirname(__file__)
locals().update(common(app=app, base=base))

INSTALLED_APPS += [  # noqa
    'sebastian.leitner',
]

ALLOWED_HOSTS += ['cards.thraxil.org']  # noqa

try:
    from local_settings import *
except ImportError:
    pass
