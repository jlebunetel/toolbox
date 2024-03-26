"""URL configuration for toolbox project."""

from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

API_PREFIX: str = f"api/v{settings.API_VERSION}/"

# Applications exposing front-end URLs:
URL_APP_LIST: list[str] = [
    "accounts",
    "anniversaries",
    "labbooks",
]


# Applications exposing API URLs:
API_APP_LIST: list[str] = [
    "accounts",
]


class ToolboxAPIRoot(APIView):
    """Application API root view."""

    def get(
        self,
        request: Request,
        format: str | None = None,  # pylint: disable=redefined-builtin
    ):
        """Build the root view."""
        del format
        return Response(
            {
                app_name: reverse(f"{app_name}_api:api-root", request=request)
                for app_name in API_APP_LIST
            }
        )


# Toolbox core front-end URLs:
urlpatterns: list[URLPattern | URLResolver] = [
    path("", include("core.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
]

# Front-end URLs for applications:
urlpatterns += [
    path(f"{app_name}/", include(f"{app_name}.urls")) for app_name in URL_APP_LIST
]

# Toolbox core API URLs:
urlpatterns += [
    path(f"{API_PREFIX}", ToolboxAPIRoot.as_view(), name="api-root"),
    path(
        f"{API_PREFIX}auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
]

# API URLs for applications:
urlpatterns += [
    path(f"{API_PREFIX}{app_name}/", include(f"{app_name}.api"))
    for app_name in API_APP_LIST
]
