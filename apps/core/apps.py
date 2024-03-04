"""Configuration of the 'core' application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class CoreConfig(AppConfig):
    """Class representing 'core' application and its configuration."""

    label: str = "core"
    name: str = "core"
    verbose_name: StrOrPromise = _("Core application")
