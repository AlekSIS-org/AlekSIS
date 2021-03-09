FROM edugit.org/AlekSIS/official/AlekSIS-Core:latest AS apps

# Install official apps
FROM core AS apps
ARG APPS="Hjelp LDAP DashboardFeeds"
ARG EXTRAS="ldap"

RUN set -e; \
    for app in $APPS; do \
        eatmydata pip install AlekSIS-App-$app\[$EXTRAS\]; \
    done

# Build assets
FROM apps as assets
RUN eatmydata aleksis-admin yarn install

# Clean up build dependencies
FROM assets AS clean
RUN set -e; \
    rm -rf /root/.cache
