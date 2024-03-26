"""Model definitions to personalize the site."""

from typing import Iterable

from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class SiteCustomization(models.Model):
    """Class on which we rely to personalize the site."""

    site = models.OneToOneField(
        Site,
        # If Site is deleted, SiteCustomization will also be deleted:
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_("site"),
    )

    is_open_for_signup = models.BooleanField(
        default=False, verbose_name=_("is open for signup")
    )

    API_THEME_CHOICES = [
        ("default", "default"),
        ("cerulean", "cerulean"),
        ("cosmo", "cosmo"),
        ("cyborg", "cyborg"),
        ("darkly", "darkly"),
        ("flatly", "flatly"),
        ("journal", "journal"),
        ("lumen", "lumen"),
        ("paper", "paper"),
        ("readable", "readable"),
        ("sandstone", "sandstone"),
        ("simplex", "simplex"),
        ("slate", "slate"),
        ("spacelab", "spacelab"),
        ("superhero", "superhero"),
        ("united", "united"),
        ("yeti", "yeti"),
    ]

    api_theme = models.CharField(
        max_length=16,
        choices=API_THEME_CHOICES,
        default="default",
        verbose_name=_("API Bootstrap theme"),
    )

    class Meta:
        """Metadata options class."""

        ordering: list[str] = ["site"]
        verbose_name: StrOrPromise = _("site customization")
        verbose_name_plural: StrOrPromise = _("site customizations")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return self.site.name or str(_("Unknown"))

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        """Saves the current instance."""
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
        Site.objects.clear_cache()  # Clear cached content
