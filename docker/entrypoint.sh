#!/bin/bash

GUNICORN_BIND=${GUNICORN_BIND:-0.0.0.0:8000}

while ! nc -z ${BISCUIT_database.host} 5432; do
    sleep 0.1
done

source /srv/venv/bin/activate

python manage.py flush --no-input
python manage.py migrate

exec /srv/venv/bin/gunicorn biscuit.core.wsgi --bind ${GUNICORN_BIND}
