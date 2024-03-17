"""Model definitions for the 'anniversaries' application."""

from uuid import uuid4

from core.models.mixins import SensitiveMixin
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

ICON_MAX_LENGTH: int = 2
TITLE_MAX_LENGTH: int = 255


class Family(SensitiveMixin, models.Model):
    """Class to represent a bunch of 'Person' instances."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    icon = models.CharField(
        max_length=ICON_MAX_LENGTH,
        default="👪",
        verbose_name=_("icon"),
        help_text=_("Pick an emoji"),
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        default=_("My family"),
        verbose_name=_("title"),
    )

    users = models.ManyToManyField(  # type: ignore
        to=settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_families",
        related_query_name="%(app_label)s_family",
        blank=True,
        verbose_name=_("users"),
        help_text=_("Users authorized to view and edit people linked to this object."),
    )

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["title"]
        verbose_name = _("family")
        verbose_name_plural = _("families")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return " ".join([self.icon, self.title]).strip()
