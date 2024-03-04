"""Configuration of the 'accounts' application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    """Class representing 'accounts' application and its configuration."""

    label: str = "accounts"
    name: str = "accounts"
    verbose_name: str = _("Authentication and Authorization")
