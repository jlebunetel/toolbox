"""View definitions for the 'anniversaries' application."""

from uuid import UUID

from anniversaries.models import Calendar
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404


def calendar_detail(
    request: HttpRequest, calendar_id: UUID, filename: str
) -> HttpResponse:
    """Return an iCalendar object."""
    del request
    calendar = get_object_or_404(Calendar, pk=calendar_id)
    response = HttpResponse(calendar.get_icalendar().decode("utf-8"))
    response.headers["Content-Type"] = "text/calendar"
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
