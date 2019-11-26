from django.db import ProgrammingError
from django.urls import path

from untisconnect.models import Terms, Schoolyear

try:
    import dashboard.views.dashboard as views

    urlpatterns = [
        path('', views.index, name='dashboard'),
        path('api', views.api_information, name="api_information"),
        path('api/notifications/read/<int:id>', views.api_read_notification, name="api_read_notification"),
        path('api/my-plan', views.api_my_plan_html, name="api_my_plan_html"),
    ]

except (Terms.DoesNotExist, Schoolyear.DoesNotExist, ProgrammingError):
    from timetable import fallback_view

    urlpatterns = [
        path('', fallback_view.fallback, name='dashboard'),
        path('api', fallback_view.fallback, name="api_information"),
        path('api/notifications/read/<int:id>', fallback_view.fallback, name="api_read_notification"),
        path('api/my-plan', fallback_view.fallback, name="api_my_plan_html"),
    ]

import dashboard.views.tools as tools_views

urlpatterns += [
    path('offline', views.offline, name='offline'),
    path("tools", tools_views.tools, name="tools"),
    path("tools/clear-cache", tools_views.tools_clear_cache, name="tools_clear_cache"),
    path("tools/clear-cache/<str:id>", tools_views.tools_clear_cache, name="tools_clear_single_cache"),
]
