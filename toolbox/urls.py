"""URL configuration for toolbox project."""

from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic import TemplateView

urlpatterns: list[URLPattern | URLResolver] = [
    path("", TemplateView.as_view(template_name="landing.html"), name="landing"),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
]
