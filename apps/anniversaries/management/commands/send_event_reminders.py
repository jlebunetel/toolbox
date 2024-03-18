"""Register 'anniversaries' actions with 'manage.py'."""

import logging
from datetime import date

from accounts.models import User
from anniversaries.models import Calendar, Person
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

DAYS_AHEAD: int = 7  # one week

logger = logging.getLogger(__name__)


def send_email(*, days: int = DAYS_AHEAD) -> None:
    """Send email"""
    current_site = Site.objects.get_current()

    for user in User.objects.filter(is_active=True):
        events: list[tuple[Person, int, date]] = []
        calendars: QuerySet[Calendar] = user.anniversaries_calendars_as_owner.all()
        for calendar in calendars:
            logger.info(
                'Send email to "%s" with event reminders linked to the calendar "%s" '
                "for the next %s day(s).",
                user,
                calendar,
                days,
            )
            events += calendar.get_next_birthday_list(days=days)

            subject: str = " ".join(
                [
                    f"[{settings.CUSTOM_SITE_NAME}]",  # type: ignore
                    "🎂",
                    _("Birthdays in the next %(days)s days") % {"days": days},
                    f"({calendar})",
                ]
            )

            send_mail(
                from_email=None,
                subject=subject,
                message=render_to_string(
                    "anniversaries/event_reminders.txt",
                    {
                        "calendar": calendar,
                        "events": events,
                        "days": days,
                        "site": current_site,
                    },
                ).strip(),
                recipient_list=[user.email],
                fail_silently=True,
                html_message=render_to_string(
                    "anniversaries/event_reminders.html",
                    {
                        "calendar": calendar,
                        "events": events,
                        "days": days,
                        "site": current_site,
                    },
                ).strip(),
            )


class Command(BaseCommand):
    """Command to send email to all users with calendar event reminders."""

    help: str = "Send event reminders"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--days", nargs="?", type=int, default=DAYS_AHEAD)

    def handle(self, *args: str, **kwargs: int) -> None:
        """Updates or creates the default site configuration and superuser."""
        del args
        try:
            send_email(days=kwargs["days"])
            self.stdout.write(self.style.SUCCESS("Successfully sent event reminders"))
        except Exception as error:
            raise CommandError(error) from error
