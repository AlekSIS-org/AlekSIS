FROM python:3.8-buster AS core

# Configure Python to be nice inside Docker and pip to stfu
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DEFAULT_TIMEOUT 100
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

# Configure app settings for build and runtime
ENV ALEKSIS_static__root /usr/share/aleksis/static
ENV ALEKSIS_media__root /var/lib/aleksis/media
ENV ALEKSIS_backup__location /var/lib/aleksis/backups

# Install necessary Debian packages for build and runtime
RUN apt-get -y update && \
    apt-get -y install eatmydata && \
    eatmydata apt-get -y upgrade && \
    eatmydata apt-get install -y --no-install-recommends \
        build-essential \
	gettext \
	libpq5 \
	libpq-dev \
	libssl-dev \
	netcat-openbsd \
	yarnpkg

# Install core
WORKDIR /usr/src/app
COPY LICENCE.rst README.rst manage.py poetry.lock pyproject.toml ./
COPY aleksis ./aleksis/
RUN set -e; \
    mkdir -p /var/lib/aleksis/media /usr/share/aleksis/static /var/lib/aleksis/backups; \
    eatmydata pip install poetry; \
    poetry config virtualenvs.create false; \
    eatmydata poetry install; \
    eatmydata pip install gunicorn django-compressor

# Declare a persistent volume for all data
VOLUME /var/lib/aleksis

# Define entrypoint and gunicorn running on port 8000
EXPOSE 8000
COPY docker/entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Install core extras
FROM core AS core-extras
ARG EXTRA_LDAP=1
ARG EXTRA_CELERY=1
WORKDIR /usr/src/app

# LDAP
RUN   if [ $EXTRA_LDAP = 1 ] ; then \
        eatmydata apt-get install -y --no-install-recommends \
        libldap2-dev \
        libsasl2-dev \
        ldap-utils; \
        eatmydata poetry install -E ldap; \
        fi;

# Celery
RUN   if [ $EXTRA_CELERY = 1 ] ; then \
        eatmydata poetry install -E celery; \
        fi;

# Install official apps
FROM core-extras AS apps
COPY apps ./apps/
RUN set -e; \
    for d in apps/official/*; do \
        cd $d; \
        rm -rf .git; \
        poetry install; \
        cd ../../..; \
    done

# Build messages and assets
FROM apps as assets
RUN eatmydata python manage.py compilemessages && \
    eatmydata python manage.py yarn install && \
    eatmydata python manage.py collectstatic --no-input --clear

# Clean up build dependencies
FROM assets AS clean
RUN set -e; \
    eatmydata apt-get remove --purge -y \
        build-essential \
        gettext \
        libpq-dev \
        libssl-dev \
        yarnpkg; \
    eatmydata apt-get autoremove --purge -y; \
    apt-get clean -y; \
    eatmydata pip uninstall -y poetry; \
    rm -f /var/lib/apt/lists/*_*; \
    rm -rf /root/.cache
