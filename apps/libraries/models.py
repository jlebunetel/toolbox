"""Model definitions for the 'libraries' application."""

import logging
import os
import shutil
from pathlib import Path
from uuid import uuid4

from core.models.mixins import SensitiveMixin
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class MediaStorage(FileSystemStorage):
    """Storage definition."""

    location = settings.MEDIA_ROOT
    base_url = settings.MEDIA_URL

    def get_available_name(self, name: str, max_length: int | None = None):
        """Removes any previously stored file (if any) before returning the name."""
        del max_length
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name


def slugify_filename(filename: str) -> str:
    """Slugify a filename"""
    name, extension = os.path.splitext(filename)
    if not extension:
        raise ValidationError("The filename does not have an extension.")
    return slugify(name) + extension


def book_folder(instance: "Book") -> str:
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    return f"{app_label}/{model_name}/{instance.id}"


def book_cover_directory_path(instance: "Book", filename: str) -> str:
    """Build directory path to store the cover of a Book models."""
    return f"{book_folder(instance)}/cover/{slugify_filename(filename)}"


def book_pdf_directory_path(instance: "Book", filename: str) -> str:
    """Build directory path to store the PDF of a Book models."""
    return f"{book_folder(instance)}/pdf/{slugify_filename(filename)}"


class Author(SensitiveMixin, models.Model):
    """Class to represent an author."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(
        max_length=1023,
        default=_("Unknown author"),
        verbose_name=_("name"),
    )

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["name"]
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return self.name


class Editor(SensitiveMixin, models.Model):
    """Class to represent an editor."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(
        max_length=1023,
        default=_("Unknown editor"),
        verbose_name=_("name"),
    )

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["name"]
        verbose_name = _("editor")
        verbose_name_plural = _("editors")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return self.name


class Book(SensitiveMixin, models.Model):
    """Class to represent a book."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(
        max_length=1023,
        default=_("My book"),
        verbose_name=_("title"),
    )

    authors = models.ManyToManyField(
        blank=True,
        to=Author,
        related_name="%(app_label)s_books",
        related_query_name="%(app_label)s_book",
        verbose_name=_("authors"),
    )

    editor = models.ForeignKey(
        blank=True,
        null=True,
        to=Editor,
        # Allow deleting the Editor only if all Book instances are deleted first:
        on_delete=models.PROTECT,
        related_name="%(app_label)s_books",
        related_query_name="%(app_label)s_book",
        verbose_name=_("editor"),
    )

    # TODO: ISBN validator
    isbn = models.CharField(
        blank=True,
        max_length=17,
        verbose_name=_("ISBN"),
    )

    # TODO: tag slugify
    tags = ArrayField(
        blank=True,
        base_field=models.CharField(
            max_length=255,
            blank=True,
        ),
        default=list,
        verbose_name=_("tags"),
    )

    pub_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("publication date"),
    )

    cover = models.ImageField(
        blank=True,
        null=False,
        upload_to=book_cover_directory_path,
        storage=MediaStorage,
        validators=[FileExtensionValidator(["jgp", "jpeg", "png"])],
        verbose_name=_("cover"),
    )

    pdf = models.FileField(
        blank=True,
        null=False,
        upload_to=book_pdf_directory_path,
        storage=MediaStorage,
        validators=[FileExtensionValidator(["pdf"])],
        verbose_name=_("PDF"),
    )

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["title"]
        verbose_name = _("book")
        verbose_name_plural = _("books")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return self.title


@receiver(models.signals.post_delete, sender=Book)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    del sender, kwargs
    shutil.rmtree(settings.MEDIA_ROOT / book_folder(instance), ignore_errors=True)
