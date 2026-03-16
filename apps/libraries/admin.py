"""Configuration of the 'libraries' application administration site."""

from typing import Any

from core.admin.mixins import SensitiveAdminMixin
from django.contrib import admin
from django.contrib.admin import TabularInline, site
from django.db.models.base import ModelBase
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import QuerySet
from django.forms.models import ModelMultipleChoiceField
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from libraries.models import Author, Book, Editor


class AuthorInline(TabularInline):
    """Options for inline editing of 'Author' instances."""

    model: ModelBase = Book.authors.through
    extra: int = 0


class AuthorAdmin(SensitiveAdminMixin, admin.ModelAdmin):
    """Encapsulate all admin options and functionality for the model 'Author'."""

    def get_readonly_fields(
        self, request: HttpRequest, obj: Book | None = None
    ) -> list[str] | tuple[Any, ...]:
        """Only allow superusers to change the creator of an object."""
        readonly_fields = ["created_at", "changed_by", "changed_at"]
        if not request.user.is_superuser:  # type: ignore
            readonly_fields.append("created_by")
        return list(super().get_readonly_fields(request, obj)) + readonly_fields


admin.site.register(Author, AuthorAdmin)


class EditorAdmin(SensitiveAdminMixin, admin.ModelAdmin):
    """Encapsulate all admin options and functionality for the model 'Editor'."""

    def get_readonly_fields(
        self, request: HttpRequest, obj: Book | None = None
    ) -> list[str] | tuple[Any, ...]:
        """Only allow superusers to change the creator of an object."""
        readonly_fields = ["created_at", "changed_by", "changed_at"]
        if not request.user.is_superuser:  # type: ignore
            readonly_fields.append("created_by")
        return list(super().get_readonly_fields(request, obj)) + readonly_fields


admin.site.register(Editor, EditorAdmin)


class BookAdmin(SensitiveAdminMixin, admin.ModelAdmin):
    """Encapsulate all admin options and functionality for the model 'Book'."""

    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("title", "isbn"),
                    ("editor", "pub_date"),
                    ("tags",),
                    (
                        "cover",
                        "pdf",
                    ),
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

    inlines = [AuthorInline]

    list_display = ("__str__", "editor", "isbn", "pub_date")

    search_fields = ("title", "tags")

    list_filter = ("editor", "authors")

    def get_queryset(self, request: HttpRequest) -> QuerySet[Book]:
        """Allowed only for the creator of the object and superusers."""
        queryset = super().get_queryset(request)
        return (
            queryset
            if request.user.is_superuser  # type: ignore
            else queryset.filter(created_by=request.user)
        )

    def get_readonly_fields(
        self, request: HttpRequest, obj: Book | None = None
    ) -> list[str] | tuple[Any, ...]:
        """Only allow superusers to change the creator of an object."""
        readonly_fields = ["created_at", "changed_by", "changed_at"]
        if not request.user.is_superuser:  # type: ignore
            readonly_fields.append("created_by")
        return list(super().get_readonly_fields(request, obj)) + readonly_fields

    def has_change_permission(
        self, request: HttpRequest, obj: Book | None = None
    ) -> bool:
        """Allowed only for the creator of the object and superusers."""
        return request.user.is_superuser or (  # type: ignore
            request.user == obj.created_by if obj else False
        )

    def has_delete_permission(
        self, request: HttpRequest, obj: Book | None = None
    ) -> bool:
        """Allowed only for the creator of the object and superusers."""
        return request.user.is_superuser or (  # type: ignore
            request.user == obj.created_by if obj else False
        )


admin.site.register(Book, BookAdmin)
