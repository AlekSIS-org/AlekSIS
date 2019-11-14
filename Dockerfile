FROM python:3.8-buster

# Configure Python to be nice inside Docker and pip to stfu
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

# Configure BiscuIT settings for build and runtime
ENV BISCUIT_static__root=/srv/static
ENV BISCUIT_media__root=/srv/media

# FIXME Use poetry pre-release for external build
ENV POETRY_VERSION=1.0.0b3

# Install necessary Debian packages for build and runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
	gettext \
	gunicorn \
	libjs-bbotstrap4 \
	libpq-dev \
	libssl-dev \
	python3-dev

# Copy the entire app directory
COPY . /usr/src/app/BiscuIT-ng

# Install BiscuIT core
WORKDIR /usr/src/app/BiscuIT-ng
RUN pip install "poetry==$POETRY_VERSION"; \
    python -m venv /srv/venv; \
    poetry export --no-dev -f requirements.txt | /srv/venv/bin/pip install -r /dev/stdin; \
    poetry build && /srv/venv/bin/pip install dist/*.whl

# Build messages and assets
RUN mkdir /srv/media /srv/static /var/backups/biscuit; \
    /srv/venv/bin/python manage.py compilemessages; \
    /srv/venv/bin/python manage.py collectstatic --no-input --clear

# Clean up build dependencies
RUN apt-get remove --purge -y \
        build-essential \
        gettext \
        libpq-dev \
        libssl-dev \
        python3-dev; \
    apt-get autoremove --purge -y; \
    apt-get clean -y; \
    rm -f /var/lib/apt/lists/*

EXPOSE 8000
ENTRYPOINT ["/usr/src/app/BiscuIT-ng/docker/entrypoint.sh"]
