#!/bin/bash

GUNICORN_BIND=${GUNICORN_BIND:-0.0.0.0:8000}

export ALEKSIS_database__host=${ALEKSIS_database__host:-127.0.0.1}
export ALEKSIS_database__port=${ALEKSIS_database__port:-5432}

if [[ -z $ALEKSIS_secret_key ]]; then
    if [[ ! -e /var/lib/aleksis/secret_key ]]; then
	touch /var/lib/aleksis/secret_key; chmod 600 /var/lib/aleksis/secret_key
	LC_ALL=C tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' </dev/urandom | head -c 64 >/var/lib/aleksis/secret_key
    fi
    ALEKSIS_secret_key=$(</var/lib/aleksis/secret_key)
fi

while ! nc -z $ALEKSIS_database__host $ALEKSIS_database__port; do
    sleep 0.1
done

python manage.py compilescss
python manage.py collectstatic --no-input --clear
python manage.py migrate
python manage.py createinitialrevisions

ARG=${$1:-"gunicorn"}

if [ $ARG = "celery_worker" ]; then
    exec celery -A aleksis.core worker -l info
elif [ $ARG = "celery_beat" ]; then
    exec celery -A aleksis.core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
else
    exec gunicorn aleksis.core.wsgi --bind ${GUNICORN_BIND}
fi
