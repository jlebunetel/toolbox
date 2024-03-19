"""Useful methods to play with calendars"""

from datetime import date, datetime, timedelta

from django.utils.timezone import get_current_timezone
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from icalendar import Calendar as ICalendar
from icalendar import Event as IEvent

from toolbox import __version__


def get_ievent_uid(*, root: str, context: str, index: int = 0) -> str:
    """Identifier generator for icalendar.Event.uid."""
    return "_".join([root, context, str(index)])


def get_icalendar(*, title: str) -> ICalendar:
    """Returns a icalendar.Calendar object."""
    ical = ICalendar()

    ical.add(
        "prodid",
        f"-//Julien Lebunetel//toolbox {__version__}//" f"{get_language().upper()}",  # type: ignore[union-attr] # noqa: E501 # pylint: disable=line-too-long
    )
    ical.add("version", "2.0")
    ical.add("calscale", "GREGORIAN")
    ical.add("method", "PUBLISH")
    ical.add("x-wr-calname", title)
    ical.add("x-wr-caldesc", title)
    ical.add("x-wr-timezone", get_current_timezone().key)  # type: ignore
    ical.add("x-published-ttl", "PT6H")
    return ical


def get_ievent(
    *,
    envent_date: date,
    uid: str,
    summary: str,
    description: str,
    created_at: date = datetime.now(),
) -> IEvent:
    """Returns an icalendar.Event object."""
    event = IEvent()
    event.add("dtstart", envent_date)
    event.add("dtend", envent_date + timedelta(days=1))
    event.add("uid", uid)
    event.add("created", created_at)
    event.add("dtstamp", created_at)
    event.add("last-modified", created_at)
    event.add("sequence", 0)
    event.add("status", "CONFIRMED")
    event.add("transp", "TRANSPARENT")
    event.add("summary", summary if summary else _("New event"))
    if description:
        event.add("description", description)
    return event


def get_anniversary_list(*, event_date: date, end_date: date) -> list[date]:
    """Returns a list of anniversary dates from the 1st anniversary date to the last
    one before 'end_date'(included)."""
    dates: list[date] = []

    for year in range(event_date.year + 1, end_date.year + 1):
        try:
            anniversary = event_date.replace(year=year)
        except ValueError:
            # Raised when the event date is February 29
            # and current year is not a leap year.
            anniversary = event_date.replace(year=year, month=3, day=1)

        if anniversary <= end_date:
            dates.append(anniversary)

    return dates
