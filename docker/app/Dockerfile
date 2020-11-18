FROM python:3.9-buster AS core

# Configure Python to be nice inside Docker and pip to stfu
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DEFAULT_TIMEOUT 100
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1
ENV PIP_EXTRA_INDEX_URL https://edugit.org/api/v4/projects/461/packages/pypi/simple

# Configure app settings for build and runtime
ENV DJANGO_SETTINGS_MODULE=aleksis.core.settings
ENV ALEKSIS_static__root /usr/share/aleksis/static
ENV ALEKSIS_media__root /var/lib/aleksis/media
ENV ALEKSIS_backup__location /var/lib/aleksis/backups

# Install necessary Debian and PyPI packages for build and runtime
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
	yarnpkg && \
    eatmydata pip install gunicorn django-compressor

# Install extra dependencies
ARG EXTRAS="celery,ldap"
RUN   if [ ",$EXTRAS," = *",ldap,"* ]; then \
        eatmydata apt-get install -y --no-install-recommends \
        libldap2-dev \
        libsasl2-dev \
        ldap-utils; \
      fi;

# Install core
RUN set -e; \
    mkdir -p /var/lib/aleksis/media /usr/share/aleksis/static /var/lib/aleksis/backups; \
    eatmydata pip install AlekSIS-Core\[$EXTRAS\]

# Declare a persistent volume for all data
VOLUME /var/lib/aleksis

# Define entrypoint and gunicorn running on port 8000
EXPOSE 8000
COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Install official apps
FROM core AS apps
ARG APPS="Hjelp LDAP DashboardFeeds"

RUN set -e; \
    for app in $APPS; do \
        eatmydata pip install AlekSIS-App-$app\[$EXTRAS\]; \
    done

# Build assets
FROM apps as assets
RUN eatmydata django-admin yarn install && \
    eatmydata django-admin collectstatic --no-input --clear

# Clean up build dependencies
FROM assets AS clean
RUN set -e; \
    eatmydata apt-get remove --purge -y \
        build-essential \
        gettext \
        libpq-dev \
        libssl-dev \
        libldap2-dev \
        libsasl2-dev \
        yarnpkg; \
    eatmydata apt-get autoremove --purge -y; \
    apt-get clean -y; \
    rm -f /var/lib/apt/lists/*_*; \
    rm -rf /root/.cache
