"""API definitions for the 'accounts' application."""

from accounts.viewsets import GroupViewset, PermissionViewset, UserViewset
from rest_framework.routers import APIRootView, DefaultRouter

app_name = "accounts_api"


class AccountsAPIRootView(APIRootView):
    """Application root view."""


class AccountsRouter(DefaultRouter):
    """Application rooter"""

    APIRootView = AccountsAPIRootView


router = AccountsRouter()
router.register("groups", GroupViewset, basename="groups")
router.register("permissions", PermissionViewset, basename="permissions")
router.register("users", UserViewset, basename="users")
urlpatterns = router.urls
