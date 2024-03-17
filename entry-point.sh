#!/usr/bin/env bash
set -e

if [[ -z "${PORT}" ]]; then
    export PORT=8000
fi

if [[ "$SETTINGS" ]]; then
    export DJANGO_SETTINGS_MODULE="$APP.$SETTINGS"
else
    export DJANGO_SETTINGS_MODULE="$APP.settings_docker"
fi

if [ "$1" == "migrate" ]; then
    exec python manage.py migrate
fi

if [ "$1" == "static" ]; then
    exec python manage.py collectstatic --verbosity 2 --noinput
fi

if [ "$1" == "shell" ]; then
    exec python manage.py shell
fi

if [ "$1" == "manage" ]; then
    # run arbitrary manage.py commands
    shift
    exec python manage.py "$@"
fi

if [ "$1" == "run" ]; then
    exec gunicorn --env DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE $APP.wsgi:application -b 0.0.0.0:8000 -w 3 --max-requests=1000 --max-requests-jitter=50 \
	--access-logfile=- --error-logfile=-

fi
