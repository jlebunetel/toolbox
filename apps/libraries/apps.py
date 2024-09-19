"""Configuration of the 'libraries' application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class LibrariesConfig(AppConfig):
    """Class representing 'libraries' application and its configuration."""

    label: str = "libraries"
    name: str = "libraries"
    verbose_name: StrOrPromise = _("Libraries")
