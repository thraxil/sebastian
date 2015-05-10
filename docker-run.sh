#!/bin/bash

cd /var/www/sebastian/sebastian/
python manage.py migrate --noinput --settings=sebastian.settings_docker
python manage.py collectstatic --noinput --settings=sebastian.settings_docker
python manage.py compress --settings=sebastian.settings_docker
exec gunicorn --env \
  DJANGO_SETTINGS_MODULE=sebastian.settings_docker \
  sebastian.wsgi:application -b 0.0.0.0:8000 -w 3 \
  --access-logfile=- --error-logfile=-
