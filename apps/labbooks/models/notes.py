"""Model definitions for the 'labbook' application."""

import json
import logging

# from random import choice
from uuid import uuid4

from core.models.mixins import SensitiveMixin
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

# from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# from markdown import markdown

# from markdown.extensions.wikilinks import WikiLinkExtension

# TITLE_MAX_LENGTH: int = 255
# SLUG_PREFIX_LENGTH: int = 7
TAG_MAX_LENGTH: int = 255

# UPPERCASE_LETTERS: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# UPPERCASE_LETTERS_EXCLUDE_SIMILAR: str = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # I O
# LOWERCASE_LETTERS: str = "abcdefghijklmnopqrstuvwxyz"
# LOWERCASE_LETTERS_EXCLUDE_SIMILAR: str = "abcdefghijkmnopqrstuvwxyz"  # l
# NUMBERS: str = "0123456789"
# NUMBERS_EXCLUDE_SIMILAR: str = "23456789"  # 0 1
# ALL_EXCLUDE_SIMILAR: str = (
#     UPPERCASE_LETTERS_EXCLUDE_SIMILAR
#     + LOWERCASE_LETTERS_EXCLUDE_SIMILAR
#     + NUMBERS_EXCLUDE_SIMILAR
# )

NO_TITLE: str = _("No title")

# def get_salt(length: int) -> str:
#     return "".join([choice(ALL_EXCLUDE_SIMILAR) for _ in range(length)])


# def get_unique_slug(
#     title: str, prefix_length: int, separator: str = "_", allow_unicode=False
# ) -> str:
#     if prefix_length < len(separator):
#         raise ValueError
#     is_unique: bool = False
#     title_slug: str = slugify(value=title, allow_unicode=allow_unicode)
#     while not is_unique:
#         slug = separator.join([get_salt(prefix_length - len(separator)), title_slug])
#         is_unique = not Note.objects.filter(slug=slug).exists()
#     return slug


logger = logging.getLogger(__name__)


def get_tags(meta: dict[str, list[str]]):
    """Returns the tags found in body metadata."""
    if "tag" in meta:
        if meta["tag"]:
            return meta["tag"]
    return []


class Note(SensitiveMixin, models.Model):
    """Class to represent a simple note."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # title = models.CharField(
    #     max_length=TITLE_MAX_LENGTH,
    #     verbose_name=_("title"),
    # )

    # slug = models.CharField(
    #     max_length=TITLE_MAX_LENGTH + SLUG_PREFIX_LENGTH,
    #     editable=False,
    #     verbose_name=_("slug"),
    # )

    body = models.TextField(
        blank=True,
        verbose_name=_("body"),
    )

    html = models.TextField(
        default="",
        editable=False,
        verbose_name=_("html"),
    )

    meta = models.JSONField(
        default=dict,
        editable=False,
        verbose_name=_("metadata"),
    )

    tags = ArrayField(
        base_field=models.CharField(
            max_length=TAG_MAX_LENGTH,
            blank=True,
        ),
        # blank=True,
        default=list,
        verbose_name=_("tags"),
    )

    # html = models.TextField(
    #     editable=False,
    #     default="",
    #     verbose_name=_("html"),
    # )

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["-changed_at"]
        verbose_name = _("note")
        verbose_name_plural = _("notes")

        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["slug", "created_by"],
        #         name="unique_slug_for_creator",
        #     )
        # ]

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return self.title

    def get_absolute_url(self):
        """Returns the canonical URL of the model."""
        # return reverse("admin:labbooks_note_change", kwargs={"object_id": self.pk})
        return reverse("labbooks:note-update", kwargs={"pk": self.pk})

    # def my_url_builder(self, label: str, base: str, end: str) -> str:
    #     del base, end
    #     try:
    #         note = Note.objects.get(title=label)
    #     except (Note.DoesNotExist, Note.MultipleObjectsReturned):
    #         return label
    #     return note.get_absolute_url()

    def clean(self) -> None:
        """Validate the model as a whole."""
        from markdown import Extension, Markdown

        extensions: list[str | Extension] = [
            "codehilite",
            "admonition",
            "extra",
            "meta",
        ]
        md = Markdown(extensions=extensions)
        self.html = md.convert(source=self.body)

        # meta: dict[str, list[str]] = md.Meta  # pylint: disable=no-member
        # self.meta = meta
        self.meta = md.Meta

        self.tags = get_tags(self.meta)

        #     # Create a new slug:
        #     if not self.slug:
        #         if not self.title:
        #             self.title = _("Untitled")
        #         self.slug = get_unique_slug(
        #             title=str(self.title),
        #             prefix_length=SLUG_PREFIX_LENGTH,
        #             separator="_",
        #             allow_unicode=False,
        #         )

        #     # Convert tags to slugs:
        #     self.tags = [slugify(value=tag, allow_unicode=True) for tag in self.tags]

        #     # Convert markdown to html:
        #     self.html = markdown(
        #         self.body,
        #         output_format="html",
        #         extensions=[
        #             WikiLinkExtension(build_url=self.my_url_builder, html_class="mesliens")
        #         ],
        #     )

        super().clean()

    @property
    @admin.display(description=_("size"), boolean=False)
    def body_length(self) -> int:
        """Returns the number of characters in the 'body' field."""
        return len(self.body)

    @property
    @admin.display(description=_("metadata"), boolean=False)
    def pretty_meta(self) -> str:
        """Pretty-print metadata."""
        return mark_safe(
            f"<pre>{json.dumps(self.meta, indent=4, sort_keys=True)}</pre>"
        )

    # @property
    # @admin.display(description=_("html"), boolean=False)
    # def pretty_html(self) -> str:
    #     """Pretty-print html."""
    #     # return mark_safe(f'<div class="toto">{self.html}</div>')
    #     return mark_safe(f'<iframe src="{self.get_absolute_url()}"></iframe>')

    @property
    def title(self) -> str:
        """Returns the first title found in body metadata."""

        if "title" in self.meta:
            if self.meta["title"]:
                # list is not empty
                return self.meta["title"][0] or str(NO_TITLE)

        return str(NO_TITLE)

    @property
    def description(self) -> str:
        """Returns the first description found in body metadata."""

        if "description" in self.meta:
            if self.meta["description"]:
                return self.meta["description"][0]

        return ""

    # @property
    # def tags(self) -> list[str]:
    #     """Returns the tags found in body metadata."""

    #     if "tag" in self.meta:
    #         if self.meta["tag"]:
    #             return self.meta["tag"]

    #     return []
