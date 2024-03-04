"""Validators for the 'accounts' application."""

from django.core.validators import RegexValidator
from django.utils.translation import gettext as _


class UsernameValidator(RegexValidator):  # pylint: disable=R# pylint: disable=R0903
    """Validate the username with a regex pattern"""

    regex = r"^[\w]+\Z"
    message: str = _(
        "Enter a valid username. This value may contain only letters, numbers, "
        "and _ character."
    )
    flags: int = 0


username_validators = [UsernameValidator()]
