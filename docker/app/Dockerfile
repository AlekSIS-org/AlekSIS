FROM registry.edugit.org/aleksis/official/aleksis-core:master AS apps

# Install official apps
FROM apps AS core
ARG APPS="Hjelp LDAP DashboardFeeds"
ARG EXTRAS="ldap"

RUN set -e; \
    for app in $APPS; do \
        eatmydata pip install AlekSIS-App-$app\[$EXTRAS\]; \
    done

# Build assets
FROM apps as assets
RUN apt update; apt install yarnpkg -y
RUN eatmydata aleksis-admin yarn install

# Clean up build dependencies
FROM assets AS clean
RUN set -e; \
    rm -rf /root/.cache
