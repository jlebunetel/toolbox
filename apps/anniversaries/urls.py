"""URL configuration for the 'anniversaries' application."""

from anniversaries.views import calendar_detail
from django.urls import URLPattern, URLResolver, path

app_name: str = "anniversaries"

urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "calendars/<uuid:calendar_id>/<str:filename>",
        calendar_detail,
        name="calendar-detail",
    ),
]
