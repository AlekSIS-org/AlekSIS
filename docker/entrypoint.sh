#!/bin/bash

GUNICORN_BIND=${GUNICORN_BIND:-0.0.0.0:8000}

export BISCUIT_database__host=${BISCUIT_database__host:-127.0.0.1}
export BISCUIT_database__port=${BISCUIT_database__port:-5432}

if [[ -z $BISCUIT_secret_key ]]; then
    if [[ ! -e /etc/biscuit/secret_key ]]; then
	touch /etc/biscuit/secret_key; chmod 600 /etc/biscuit/secret_key
	LC_ALL=C tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' </dev/urandom | head -c 64 >/etc/biscuit/secret_key
    fi
    BISCUIT_secret_key=$(</etc/biscuit/secret_key)
fi

while ! nc -z $BISCUIT_database__host $BISCUIT_database__port; do
    sleep 0.1
done

python manage.py flush --no-input
python manage.py migrate

exec gunicorn biscuit.core.wsgi --bind ${GUNICORN_BIND}
