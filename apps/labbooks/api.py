"""API definitions for the 'labbooks' application."""

from rest_framework.routers import APIRootView, DefaultRouter

app_name = "labbooks_api"


class LabbooksAPIRootView(APIRootView):
    """Application root view."""


class LabbooksRouter(DefaultRouter):
    """Application rooter"""

    APIRootView = LabbooksAPIRootView


router = LabbooksRouter()
urlpatterns = router.urls
