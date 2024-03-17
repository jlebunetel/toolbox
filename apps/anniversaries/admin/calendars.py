"""Configuration of the 'anniversaries' application administration site."""

from typing import Any

from anniversaries.models import Calendar, Family
from core.admin.mixins import SensitiveAdminMixin
from django.contrib import admin
from django.db.models import Q
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import QuerySet
from django.forms.models import ModelMultipleChoiceField
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class CalendarAdmin(SensitiveAdminMixin, admin.ModelAdmin):
    """Encapsulate all admin options and functionality for the model 'Calendar'."""

    @admin.display(description=_("families"))
    def _families(self, obj: Calendar) -> str:
        """Returns the list of concerned families."""
        return format_html("<br/>".join([str(family) for family in obj.families.all()]))

    @admin.display(description=_("URL"))
    def _url(self, obj: Calendar) -> str:
        """Returns the URL of the iCalendar file."""
        absolute_url = obj.get_absolute_url()
        return format_html(f'<a href={absolute_url} target="_blank">{absolute_url}</a>')

    list_display = (
        "__str__",
        "_families",
        "years_ahead",
        "_url",
    )

    list_filter = (("families", admin.RelatedOnlyFieldListFilter),)

    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("icon", "title"),
                    ("families",),
                ],
            },
        ),
        (
            _("Advanced options"),
            {
                "classes": ["collapse"],
                "fields": [
                    "years_ahead",
                    "hide_death_anniversaries",
                    ("created_by", "created_at"),
                    ("changed_by", "changed_at"),
                ],
            },
        ),
    ]

    filter_horizontal = ("families",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Calendar]:
        """Allowed only for the creator of the object and superusers."""
        queryset = super().get_queryset(request)
        return (
            queryset
            if request.user.is_superuser  # type: ignore
            else queryset.filter(created_by=request.user)
        )

    def get_readonly_fields(
        self, request: HttpRequest, obj: Calendar | None = None
    ) -> list[str] | tuple[Any, ...]:
        """Only allow superusers to change the creator of an object."""
        readonly_fields = ["created_at", "changed_by", "changed_at"]
        if not request.user.is_superuser:  # type: ignore
            readonly_fields.append("created_by")
        return list(super().get_readonly_fields(request, obj)) + readonly_fields

    def formfield_for_manytomany(
        self,
        db_field: ManyToManyField,
        request: HttpRequest,
        **kwargs: Any,
    ) -> ModelMultipleChoiceField | None:
        """If not superuser, filter by creator and authorized users."""
        if db_field.name == "families" and request:
            kwargs["queryset"] = (
                Family.objects.all()
                if request.user.is_superuser  # type: ignore
                else Family.objects.filter(
                    Q(created_by=request.user) | Q(users__in=[request.user])
                ).distinct()
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def has_change_permission(
        self, request: HttpRequest, obj: Calendar | None = None
    ) -> bool:
        """Allowed only for the creator of the object and superusers."""
        return request.user.is_superuser or (  # type: ignore
            request.user == obj.created_by if obj else False
        )

    def has_delete_permission(
        self, request: HttpRequest, obj: Calendar | None = None
    ) -> bool:
        """Allowed only for the creator of the object and superusers."""
        return request.user.is_superuser or (  # type: ignore
            request.user == obj.created_by if obj else False
        )


admin.site.register(Calendar, CalendarAdmin)
