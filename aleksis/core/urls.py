from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

import calendarweek.django
import debug_toolbar
from django_js_reverse.views import urls_js
from two_factor.urls import urlpatterns as tf_urls

from . import views

urlpatterns = [
    path("", include("pwa.urls"), name="pwa"),
    path("offline/", views.offline, name="offline"),
    path("admin/", admin.site.urls),
    path("data_management/", views.data_management, name="data_management"),
    path("status/", views.system_status, name="system_status"),
    path("school_management", views.school_management, name="school_management"),
    path("school/information/edit", views.edit_school, name="edit_school_information"),
    path("school/term/edit", views.edit_schoolterm, name="edit_school_term"),
    path("", include(tf_urls)),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("persons", views.persons, name="persons"),
    path("persons/accounts", views.persons_accounts, name="persons_accounts"),
    path("person", views.person, name="person"),
    path("person/<int:id_>", views.person, name="person_by_id"),
    path("person/<int:id_>/edit", views.edit_person, name="edit_person_by_id"),
    path("groups", views.groups, name="groups"),
    path("group/create", views.edit_group, name="create_group"),
    path("group/<int:id_>", views.group, name="group_by_id"),
    path("group/<int:id_>/edit", views.edit_group, name="edit_group_by_id"),
    path("", views.index, name="index"),
    path("notifications/mark-read/<int:id_>", views.notification_mark_read, name="notification_mark_read"),
    path("announcements/", views.announcements, name="announcements"),
    path("announcement/create/", views.announcement_form, name="add_announcement"),
    path("announcement/edit/<int:pk>/", views.announcement_form, name="edit_announcement"),
    path("announcement/delete/<int:pk>/", views.delete_announcement, name="delete_announcement"),
    path("maintenance-mode/", include("maintenance_mode.urls")),
    path("impersonate/", include("impersonate.urls")),
    path("__i18n__/", include("django.conf.urls.i18n")),
    path("select2/", include("django_select2.urls")),
    path("jsreverse.js", urls_js, name='js_reverse'),
    path("calendarweek_i18n.js", calendarweek.django.i18n_js, name="calendarweek_i18n_js"),
    path('gettext.js', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

# Serve static files from STATIC_ROOT to make it work with runserver
# collectstatic is also required in development for this
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files from MEDIA_ROOT to make it work with runserver
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add URLs for optional features
if hasattr(settings, "TWILIO_ACCOUNT_SID"):
    from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls  # noqa

    urlpatterns += [path("", include(tf_twilio_urls))]

# Serve javascript-common if in development
if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

# Automatically mount URLs from all installed AlekSIS apps
for app_config in apps.app_configs.values():
    if not app_config.name.startswith("aleksis.apps."):
        continue

    try:
        urlpatterns.append(path("app/%s/" % app_config.label, include("%s.urls" % app_config.name)))
    except ModuleNotFoundError:
        # Ignore exception as app just has no URLs
        pass  # noqa
