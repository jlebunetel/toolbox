"""Configuration of the 'labbooks' application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class LabbooksConfig(AppConfig):
    """Class representing 'labbooks' application and its configuration."""

    label: str = "labbooks"
    name: str = "labbooks"
    verbose_name: StrOrPromise = _("Labbooks")
