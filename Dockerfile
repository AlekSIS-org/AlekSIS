FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
ENV POETRY_VERSION=1.0.0b3

WORKDIR /usr/src/app

COPY . BiscuIT-ng

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /srv/venv

RUN apt update && apt install -y build-essential libpq-dev libssl-dev python3-dev gettext

WORKDIR ./BiscuIT-ng
RUN poetry export -f requirements.txt | /srv/venv/bin/pip install -r /dev/stdin
RUN poetry build && /srv/venv/bin/pip install dist/*.whl

WORKDIR /usr/src/app/BiscuIT-ng

RUN apt install -y libjs-bootstrap4 fonts-font-awesome libjs-jquery libjs-popper.js libjs-jquery-datatables

RUN mkdir /srv/media /srv/static /var/backups/biscuit

ENV BISCUIT_static.root=/srv/static
ENV BISCUIT_media.root=/srv/media

RUN /srv/venv/bin/python manage.py collectstatic --no-input --clear
RUN /srv/venv/bin/python manage.py compilemessages

RUN /srv/venv/bin/pip install gunicorn

EXPOSE 8000
ENTRYPOINT ["/usr/src/app/BiscuIT-ng/docker/entrypoint.sh"]
