"""URL configuration for the 'core' application."""

from django.templatetags.static import static
from django.urls import URLPattern, URLResolver, path
from django.views.generic.base import RedirectView

app_name: str = "core"

urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "favicon.svg",
        RedirectView.as_view(url=static("core/img/favicon.svg")),
        name="favicon",
    ),
    path(
        "favicon.ico",
        RedirectView.as_view(url="favicon.svg"),
    ),
]
