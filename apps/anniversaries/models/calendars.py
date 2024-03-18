"""Model definitions for the 'anniversaries' application."""

import logging
from datetime import date, datetime, timedelta
from uuid import uuid4

from anniversaries.utils import get_icalendar
from core.models.mixins import SensitiveMixin
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .families import Family
from .persons import Person

YEARS_AHEAD: int = 3
logger = logging.getLogger(__name__)


class Calendar(SensitiveMixin, models.Model):
    """Class to generate a calendar with people anniversaries."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    icon = models.CharField(
        max_length=2,
        default="🎂",
        verbose_name=_("icon"),
        help_text=_("Pick a valid emoji"),
    )

    title = models.CharField(
        max_length=255,
        default=_("My calendar"),
        verbose_name=_("title"),
    )

    hide_death_anniversaries = models.BooleanField(
        default=True,
        verbose_name=_("hide death anniversaries?"),
        help_text=_("Should we hide death anniversaries in this calendar?"),
    )

    years_ahead = models.PositiveSmallIntegerField(
        default=YEARS_AHEAD,
        verbose_name=_("years ahead"),
        help_text=_("How many years into the future should we display birthdays?"),
    )

    families = models.ManyToManyField(  # type: ignore
        to=Family,
        related_name="%(app_label)s_calendars",
        related_query_name="%(app_label)s_calendar",
        verbose_name=_("families"),
    )

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["title"]
        verbose_name = _("calendar")
        verbose_name_plural = _("calendars")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return " ".join([self.icon, self.title])

    def people(self) -> models.QuerySet[Person]:
        """Returns a queryset with people related to an instance of the model."""
        return Person.objects.filter(families__in=self.families.all()).distinct()

    def get_absolute_url(self) -> str:
        """Calculates the canonical URL for an instance of the model."""
        filename: str = slugify(self.title) + ".ics"
        return reverse(
            "anniversaries:calendar-detail",
            kwargs={"calendar_id": self.pk, "filename": filename},
        )

    def get_icalendar(self) -> bytes:
        """Builds the iCalendar."""
        ical = get_icalendar(title=str(self))
        now = datetime.now()
        # The end of the year in a few years:
        end_date = date(year=now.year + self.years_ahead, month=12, day=31)

        for person in self.people():
            for ievent in person.get_birthday_ievent_list(end_date=end_date):
                ical.add_component(ievent)

            if not self.hide_death_anniversaries:
                for ievent in person.get_death_anniversary_ievent_list(
                    end_date=end_date
                ):
                    ical.add_component(ievent)

        return ical.to_ical()

    def get_next_birthday_list(self, days: int) -> list[tuple[Person, int, date]]:
        """Returns the list of birthdays from today to "days" in the future."""
        events: list[tuple[Person, int, date]] = []
        today = date.today()
        for person in self.people():
            birthday_list = person.get_birthday_list(
                end_date=today + timedelta(days=days)
            )
            next_birthday_list = [
                (person, age, day)
                for age, day in enumerate(birthday_list)
                if day > today
            ]
            events += next_birthday_list
        return events
