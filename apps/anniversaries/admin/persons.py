"""Configuration of the 'anniversaries' application administration site."""

import logging
from typing import Any

from anniversaries.models import Family, Person
from core.admin.mixins import SensitiveAdminMixin
from django.contrib import admin
from django.db.models import Q
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import QuerySet
from django.forms.models import ModelMultipleChoiceField
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class IsAliveListFilter(admin.SimpleListFilter):
    """A class to filter based on whether the person is alive or not."""

    title = _("is alive?")

    parameter_name = "alive"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        """Choice list."""
        del request, model_admin
        return [
            ("yes", str(_("❤️ alive"))),
            ("no", str(_("🪦 dead"))),
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        """Returns the filtered queryset."""
        del request
        if self.value() == "yes":
            return queryset.filter(date_of_death__isnull=True)
        if self.value() == "no":
            return queryset.filter(date_of_death__isnull=False)
        return queryset


class PersonAdmin(SensitiveAdminMixin, admin.ModelAdmin):
    """Encapsulate all admin options and functionality for the model 'Person'."""

    @admin.display(description=_("age"), ordering="-date_of_birth")
    def _age(self, obj: Person) -> int | None:
        """Returns the current age of the person."""
        return obj.get_current_age()

    @admin.display(description=_("families"))
    def _families(self, obj: Person) -> str:
        """Returns the list of families in which the individual appears."""
        return format_html("<br/>".join([str(family) for family in obj.families.all()]))

    list_display = (
        "__str__",
        "_age",
        "nickname",
        "first_name",
        "middle_names",
        "birth_name",
        "married_name",
        "preferred_name",
        "sex",
        "date_of_birth",
        "_families",
    )

    list_filter = (
        ("families", admin.RelatedOnlyFieldListFilter),
        "sex",
        "birth_name",
        "married_name",
        "species",
        IsAliveListFilter,
    )

    search_fields = (
        "nickname",
        "first_name",
        "middle_names",
        "birth_name",
        "married_name",
        "preferred_name",
    )

    filter_horizontal = ("families",)

    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("nickname",),
                    ("first_name", "middle_names"),
                    ("birth_name", "married_name", "preferred_name"),
                    ("date_of_birth", "sex", "species"),
                    ("families",),
                ],
            },
        ),
        (
            _("Advanced options"),
            {
                "classes": ["collapse"],
                "fields": [
                    "date_of_death",
                    ("created_by", "created_at"),
                    ("changed_by", "changed_at"),
                ],
            },
        ),
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Person]:
        """If not superuser, filter by creator and authorized users."""
        queryset = super().get_queryset(request)
        return (
            queryset
            if request.user.is_superuser  # type: ignore
            else queryset.filter(
                Q(created_by=request.user) | Q(families__users__in=[request.user])
            ).distinct()
        )

    def get_readonly_fields(
        self, request: HttpRequest, obj: Person | None = None
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

    def has_delete_permission(
        self, request: HttpRequest, obj: Person | None = None
    ) -> bool:
        """Allowed only for the creator of the object and superusers."""
        return request.user.is_superuser or (  # type: ignore
            request.user == obj.created_by if obj else False
        )


admin.site.register(Person, PersonAdmin)
