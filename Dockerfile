ARG APPS="AlekSIS-App-Alsijil AlekSIS-App-Chronos AlekSIS-App-CSVImport AlekSIS-App-Hjelp AlekSIS-App-LDAP AlekSIS-App-DashboardFeeds AlekSIS-App-Untis"
ARG BUILD_DEPS="libmariadb-dev gcc python3-dev"
ARG SYSTEM_DEPS=""

FROM registry.edugit.org/aleksis/official/aleksis-core:master
