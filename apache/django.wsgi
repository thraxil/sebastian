import os, sys
import site
from os.path import *

site.addsitedir(join(dirname(__file__), "../ve/lib/python2.5/site-packages"))
sys.path.append(join(dirname(__file__),"../"))
sys.path.append('/home/anders/code/python/sebastian/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'sebastian.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
