"""Generic model mixins."""

from accounts.models import get_sentinel_user
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class SensitiveMixin(models.Model):
    """Mixin to enhance the security on sensitive models."""

    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        # If the related user is deleted, sets the creator to the "deleted" user:
        on_delete=models.SET(get_sentinel_user),
        limit_choices_to={"is_active": True},
        related_name="%(app_label)s_%(class)ss_as_owner",
        related_query_name="%(app_label)s_%(class)s_as_owner",
        verbose_name=_("creator"),
        help_text=_("The creator of this very object."),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("creation date"),
        help_text=_("When was this object created?"),
    )

    changed_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        # If the related user is deleted, sets the editor to the "deleted" user:
        on_delete=models.SET(get_sentinel_user),
        limit_choices_to={"is_active": True},
        related_name="%(app_label)s_%(class)ss_as_changed_by",
        related_query_name="%(app_label)s_%(class)s_as_changed_by",
        verbose_name=_("last editor"),
        help_text=_("Who last modified this object?"),
    )

    changed_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("last modification date"),
        help_text=_("When was this object last modified?"),
    )

    class Meta:
        """Metadata options class."""

        abstract = True
