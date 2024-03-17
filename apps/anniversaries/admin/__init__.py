"""Configuration of the 'anniversaries' application administration site."""

from .calendars import Calendar
from .families import FamilyAdmin
from .persons import PersonAdmin

__all__ = [
    "Calendar",
    "FamilyAdmin",
    "PersonAdmin",
]
