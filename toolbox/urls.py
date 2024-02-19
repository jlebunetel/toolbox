"""URL configuration for toolbox project."""
from typing import Any

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns: list[Any] = [
    path("", TemplateView.as_view(template_name="landing.html"), name="landing"),
    path("admin/", admin.site.urls),
]
