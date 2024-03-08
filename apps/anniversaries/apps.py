"""Configuration of the 'anniversaries' application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class AnniversariesConfig(AppConfig):
    """Class representing 'anniversaries' application and its configuration."""

    label: str = "anniversaries"
    name: str = "anniversaries"
    verbose_name: StrOrPromise = _("Anniversaries application")
