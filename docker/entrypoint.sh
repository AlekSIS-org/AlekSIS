#!/bin/bash

GUNICORN_BIND=${GUNICORN_BIND:-0.0.0.0:8000}
POSTGRES_HOST=${BISCUIT_database__host:-127.0.0.1}
POSTGRES_PORT=${BISCUIT_database__port:-5432}

[[ -n $POSTGRES_PASSWORD ]] && BISCUIT_database__password=$POSTGRES_PASSWORD

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

source /srv/venv/bin/activate

python manage.py flush --no-input
python manage.py migrate

exec /srv/venv/bin/gunicorn biscuit.core.wsgi --bind ${GUNICORN_BIND}
