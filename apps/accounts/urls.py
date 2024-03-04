"""URL configuration for the 'accounts' application."""

from accounts import views
from django.urls import URLPattern, URLResolver, path

app_name: str = "accounts"

urlpatterns: list[URLPattern | URLResolver] = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
