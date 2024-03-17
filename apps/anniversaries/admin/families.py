"""Configuration of the 'anniversaries' application administration site."""

import logging
from typing import Any

from anniversaries.models import Family, Person
from core.admin.mixins import SensitiveAdminMixin
from django.contrib import admin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class FamilyAdmin(SensitiveAdminMixin, admin.ModelAdmin):
    """Encapsulate all admin options and functionality for the model 'Family'."""

    @admin.display(description=_("persons"))
    def _person_number(self, obj: Family) -> int | None:
        """Returns the number of people in a family."""
        return obj.anniversaries_family_members.distinct().count()

    @admin.display(description=_("users"))
    def _users(self, obj: Person) -> str:
        """Returns the list of users involved in this family."""
        return format_html("<br/>".join([str(user) for user in obj.users.all()]))

    list_display = ("__str__", "_person_number", "created_by", "_users")

    list_filter = ("created_by",)

    search_fields = ("title",)

    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("icon", "title"),
                    "users",
                ],
            },
        ),
        (
            _("Advanced options"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("created_by", "created_at"),
                    ("changed_by", "changed_at"),
                ],
            },
        ),
    ]

    filter_horizontal = ("users",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Family]:
        """If not superuser, filter by creator and authorized users."""
        queryset = super().get_queryset(request)
        return (
            queryset
            if request.user.is_superuser  # type: ignore
            else queryset.filter(
                Q(created_by=request.user) | Q(users__in=[request.user])
            )
        )

    def get_readonly_fields(
        self, request: HttpRequest, obj: Family | None = None
    ) -> list[str] | tuple[Any, ...]:
        """Only allow superusers to change the creator of an object."""
        readonly_fields = ["created_at", "changed_by", "changed_at"]
        if not request.user.is_superuser:  # type: ignore
            readonly_fields.append("created_by")
        return list(super().get_readonly_fields(request, obj)) + readonly_fields

    def has_change_permission(
        self, request: HttpRequest, obj: Family | None = None
    ) -> bool:
        """Allowed only for the creator of the object and superusers."""
        return request.user.is_superuser or (  # type: ignore
            request.user == obj.created_by if obj else False
        )

    def has_delete_permission(
        self, request: HttpRequest, obj: Family | None = None
    ) -> bool:
        """Allowed only for the creator of the object and superusers."""
        return request.user.is_superuser or (  # type: ignore
            request.user == obj.created_by if obj else False
        )


admin.site.register(Family, FamilyAdmin)
