#!/bin/bash

GUNICORN_BIND=${GUNICORN_BIND:-0.0.0.0:8000}
POSTGRES_HOST=${POSTGRES_HOST:-127.0.0.1}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
POSTGRES_DB=${POSTGRES_DB:-biscuit}
POSTGRES_USER=${POSTGRES_USER:-biscuit}

BISCUIT_database__host=${BISCUIT_database__host:-$POSTGRES_HOST}
BISCUIT_database__port=${BISCUIT_database__port:-$POSTGRES_PORT}
BISCUIT_database__name=${BISCUIT_database__name:-$POSTGRES_DB}
BISCUIT_database__user=${BISCUIT_database__user:-$POSTGRES_USER}
BISCUIT_database__password=${BISCUIT_database__password:-$POSTGRES_PASSWORD}

while ! nc -z $BISCUIT_database__host $BISCUIT_database__port; do
    sleep 0.1
done

source /srv/venv/bin/activate

python manage.py flush --no-input
python manage.py migrate

exec /srv/venv/bin/gunicorn biscuit.core.wsgi --bind ${GUNICORN_BIND}