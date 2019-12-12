FROM python:3.8-buster

# Configure Python to be nice inside Docker and pip to stfu
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DEFAULT_TIMEOUT 100
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

# Configure app settings for build and runtime
ENV BISCUIT_static__root /var/lib/biscuit/static
ENV BISCUIT_media__root /var/lib/biscuit/media
ENV BISCUIT_backup__location /var/lib/biscuit/backups

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

# Install core dependnecies
WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml ./
RUN eatmydata pip install poetry; \
    poetry export -f requirements.txt | eatmydata pip install -r /dev/stdin; \
    eatmydata pip install gunicorn

# Install core
COPY biscuit ./biscuit/
COPY LICENCE README.rst manage.py ./
RUN mkdir -p /var/lib/biscuit/media /var/lib/biscuit/static /var/lib/biscuit/backups; \
    poetry build && eatmydata pip install dist/*.whl

# Build messages and assets
RUN python manage.py compilemessages; \
    eatmydata python manage.py yarn install

# Clean up build dependencies
RUN eatmydata apt-get remove --purge -y \
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

# Declare a persistent volume for all data
VOLUME /var/lib/biscuit

# Define entrypoint and gunicorn running on port 8000
EXPOSE 8000
COPY docker/entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
