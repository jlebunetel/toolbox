"""Configuration of the 'accounts' application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class AccountsConfig(AppConfig):
    """Class representing 'accounts' application and its configuration."""

    label: str = "accounts"
    name: str = "accounts"
    verbose_name: StrOrPromise = _("Authentication and Authorization")
