"""Model definitions for the 'accounts' application."""

from accounts.validators import UsernameValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Users within the Django authentication system are represented by this model.

    Username and password are required. Other fields are optional."""

    username_validator = UsernameValidator()

    username = models.CharField(
        _("username"),
        primary_key=True,
        max_length=20,
        unique=True,
        help_text=_("Required. 20 characters or fewer. Letters, digits and _ only."),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )

    first_name = models.CharField(_("first name"), max_length=255, blank=True)

    last_name = models.CharField(_("last name"), max_length=255, blank=True)

    class Meta(AbstractUser.Meta):  # type: ignore
        """Metadata options class."""

        ordering: list[str] = ["-date_joined"]

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        if self.first_name or self.last_name:
            return " ".join([self.first_name, self.last_name])
        return self.username

    def get_absolute_url(self) -> str:
        """Calculates the canonical URL for an object."""
        return reverse("accounts:profile")


def get_sentinel_user() -> User:
    """Returns the sentinel (or deleted) user. Creates it if required."""
    user, _ = User.objects.get_or_create(username="deleted", is_active=False)
    return user  # type: ignore[return-value]
