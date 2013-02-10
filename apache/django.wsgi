import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/sebastian/sebastian/ve/lib/python2.7/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/')
sys.path.append('/var/www/sebastian/')
sys.path.append('/var/www/sebastian/sebastian/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'sebastian.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
