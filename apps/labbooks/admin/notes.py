"""Configuration of the 'labbooks' application administration site."""

import logging

# from typing import Any
from core.admin.mixins import SensitiveAdminMixin

# from django import forms
from django.contrib import admin

# from django.db.models.query import QuerySet
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from labbooks.models import Note

logger = logging.getLogger(__name__)


# class MarkdownTextarea(forms.Textarea):
#     pass


# class NoteAdminForm(forms.ModelForm):
#     html = forms.CharField(widget=MarkdownTextarea(attrs={"class": "markdown"}))
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)

#     #     logger.debug(self.fields)
#     #     logger.debug(self.base_fields)
#     #     logger.debug(dir(self))

#     #     if "html" in self.fields:
#     #         self.fields["html"].widget.attrs["class"] = "markdown"

#     class Meta:
#         model = Note
#         fields = "__all__"
#         # widgets = {"html": forms.Textarea(attrs={"class": "markdown"})}


# def clean_slug(self) -> str:
#     title = self.cleaned_data.get("title", str(_("Untitled")))
#     slug = slugify(value=title, allow_unicode=True)

#     # The QueryDicts is immutable:
#     data = self.data.copy()
#     data["slug"] = slug
#     self.data = data

#     return slug

# def clean(self, *args, **kwargs) -> dict[str, Any]:
#     logger.debug(self.data)
#     logger.debug(self.cleaned_data)

#     title = self.cleaned_data.get("title", "")
#     slug = self.cleaned_data.get("slug", "")

#     if not title:
#         title = str(_("Untitled"))
#         # The QueryDicts is immutable:
#         data = self.data.copy()
#         data["title"] = title
#         self.data = data

#         self.cleaned_data["title"] = title

#     if not slug:
#         slug = slugify(value=title, allow_unicode=True)

#         self.cleaned_data["slug"] = slug

#         # The QueryDicts is immutable:
#         data = self.data.copy()
#         data["slug"] = slug
#         self.data = data

#     cleaned_data = super().clean(*args, **kwargs)
#     return cleaned_data

# def clean(self):
#     logger.debug(self.cleaned_data)
#     logger.debug(self.data)

#     if "title" in self.data:
#         self.data["slug"] = slugify(value=self.data["title"], allow_unicode=True)

#     # if 'title' in self.data:

#     # self.data["slug"] = slugify(
#     #     value=self.cleaned_data["slug"], allow_unicode=True
#     # )


# class TagsListFilter(admin.SimpleListFilter):
#     title = _("tags")
#     parameter_name = "tag"

#     def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
#         tags = Note.objects.values_list("tags", flat=True)
#         tags = [(tag, tag) for sublist in tags for tag in sublist if tag]
#         tags = sorted(set(tags))
#         return tags

#     def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
#         tag = self.value()
#         if tag:
#             queryset = queryset.filter(tags__contains=[tag])
#         return queryset


class NoteAdmin(SensitiveAdminMixin, admin.ModelAdmin):
    """Encapsulate all admin options and functionality for the model 'Note'."""

    # @admin.display(description=_("tags"))
    # def _tags_html(self, obj: Note) -> str:
    #     return format_html(
    #         ", ".join([f'<a href="?tag={tag}">{tag}</a>' for tag in obj.tags])
    #     )

    readonly_fields = (
        "html",
        # "slug",
        "pretty_meta",
        "created_by",
        "created_at",
        "changed_by",
        "changed_at",
    )

    list_display = (
        "__str__",
        # "_tags_html",
        "body_length",
        "created_by",
        "created_at",
        "changed_by",
        "changed_at",
    )

    # list_filter = (TagsListFilter,)

    # search_fields = ("title", "body")

    # form = NoteAdminForm

    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("body",),
                    ("pretty_meta",),
                    ("html",),
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


admin.site.register(Note, NoteAdmin)
