"""View definitions for the 'core' application."""

import logging
from datetime import date
from typing import Any

from accounts.models import User
from anniversaries.models import Calendar, Family, Person
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)

UPCOMING_DAYS: int = 15


class LandingPageView(TemplateView):
    """The landing page."""

    template_name = "core/landing.html"

    def get_context_data(self, **kwargs: int) -> dict[str, Any]:
        """Returns a dictionary representing the template context."""
        context = super().get_context_data(**kwargs)

        # Add context data for stats:
        context["stats"] = {
            _("users"): User.objects.filter(is_active=True).count(),
            _("calendars"): Calendar.objects.all().count(),
            _("families"): Family.objects.all().count(),
            _("people"): Person.objects.all().count(),
        }

        # Add context data for anniversaries:
        context["upcoming_days"] = UPCOMING_DAYS
        if user := self.request.user:
            if user.is_authenticated:
                events: list[tuple[Person, int, date]] = []
                calendars: QuerySet[Calendar] = (
                    user.anniversaries_calendars_as_owner.all()  # type: ignore
                )
                for calendar in calendars:
                    events += calendar.get_next_birthday_list(days=UPCOMING_DAYS)
                context["upcoming_birthdays"] = events

        return context
