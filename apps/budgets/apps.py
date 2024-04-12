"""Configuration of the 'budgets' application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class BudgetsConfig(AppConfig):
    """Class representing 'budgets' application and its configuration."""

    label: str = "budgets"
    name: str = "budgets"
    verbose_name: StrOrPromise = _("Budgets")
