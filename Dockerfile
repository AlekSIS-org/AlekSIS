FROM python:3.8-buster

MAINTAINER Teckisd e.V. <foss@teckids.org>

# Configure Python to be nice inside Docker and pip to stfu
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DEFAULT_TIMEOUT 100
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

# Configure app settings for build and runtime
ENV BISCUIT_static__root /srv/static
ENV BISCUIT_media__root /srv/media

# FIXME Use poetry pre-release for external build
ENV POETRY_VERSION 1.0.0b3

# Install necessary Debian packages for build and runtime
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
	gettext \
	gunicorn \
	libjs-bootstrap4 \
	libpq5 \
	libpq-dev \
	libssl-dev \
	netcat-openbsd \
	python3-dev

# Install core dependnecies
WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml ./
RUN pip install "poetry==$POETRY_VERSION"; \
    poetry export -f requirements.txt | pip install -r /dev/stdin

# Install core
COPY LICENSE README.md biscuit manage.py ./
RUN mkdir /etc/biscuit /srv/media /srv/static /var/backups/biscuit; \
    poetry build && pip install dist/*.whl

# Build messages and assets
RUN python manage.py compilemessages; \
    python manage.py collectstatic --no-input --clear

# Clean up build dependencies
RUN apt-get remove --purge -y \
        build-essential \
        gettext \
        libpq-dev \
        libssl-dev \
        python3-dev; \
    apt-get autoremove --purge -y; \
    apt-get clean -y; \
    rm -f /var/lib/apt/lists/*_*

# Mark configuration as mountableg from the host
VOLUME /etc/biscuit

# Define entrypoint and gunicorn running on port 8000
EXPOSE 8000
ENTRYPOINT ["/usr/src/app/BiscuIT-ng/docker/entrypoint.sh"]
