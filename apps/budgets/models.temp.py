"""Model definitions for the 'budgets' application."""

import logging
from datetime import date
from decimal import Decimal
from enum import Enum
from uuid import uuid4

from core.models.mixins import SensitiveMixin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from pydantic import BaseModel

ICON_MAX_LENGTH: int = 2
TITLE_MAX_LENGTH: int = 255

logger = logging.getLogger(__name__)


class ItemType(str, Enum):
    """Available item types."""

    DEBIT = "D"
    CREDIT = "C"

    @classmethod
    def get_choices(cls) -> dict[str, str]:
        """Returns a dict to use as choices in a Django model field."""
        return {i.value: i.name for i in cls}


class Currency(str, Enum):
    """Available currencies."""

    EUR = "EUR"
    USD = "USD"
    BTC = "BTC"

    @classmethod
    def get_choices(cls) -> dict[str, str]:
        """Returns a dict to use as choices in a Django model field."""
        return {i.value: i.name for i in cls}


class Entry(BaseModel):
    """Unit entry."""

    event_date: date
    item_title: str
    account: str
    item_type: ItemType
    amount: Decimal
    currency: Currency


class Category(SensitiveMixin, models.Model):
    """Class to represent a bunch of accounts."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    icon = models.CharField(
        max_length=ICON_MAX_LENGTH,
        default="📔",
        verbose_name=_("icon"),
        help_text=_("Pick an emoji."),
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        default=_("New category"),
        verbose_name=_("title"),
    )

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["title"]
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return " ".join([self.icon, self.title]).strip()


class Account(SensitiveMixin, models.Model):
    """Class to represent an account."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    category = models.ForeignKey(
        to=Category,
        # Allow deleting the Category only if all Account instances are deleted first:
        on_delete=models.PROTECT,
        related_name="accounts",
        related_query_name="account",
        verbose_name=_("category"),
    )

    icon = models.CharField(
        max_length=ICON_MAX_LENGTH,
        default="📑",
        verbose_name=_("icon"),
        help_text=_("Pick an emoji."),
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        default=_("New account"),
        verbose_name=_("title"),
    )

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["title"]
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return " ".join([str(self.category), ">", self.icon, self.title]).strip()


class Ledger(SensitiveMixin, models.Model):
    """Class to represent a book of accounts containing the summaries of debit and
    credit entries."""


class Balance(SensitiveMixin, models.Model):
    """Permet de définir le solde d'un compte à une date donnée."""

    # ledger
    # account
    # date
    # amount

    # unique : account / date


class Item(SensitiveMixin, models.Model):
    """Class to represent a simple item."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        default=_("New item"),
        verbose_name=_("title"),
    )

    account = models.ForeignKey(
        to=Account,
        # Allow deleting the Account only if all Item instances are deleted first:
        on_delete=models.PROTECT,
        related_name="items",
        related_query_name="item",
        verbose_name=_("account"),
    )

    item_type = models.CharField(
        max_length=1,
        choices=ItemType.get_choices(),
        default=ItemType.DEBIT,
        verbose_name=_("type"),
        help_text=_(
            "Does this transaction have a positive (credit) or negative (debit) impact "
            "on your balance?"
        ),
    )

    amount = models.DecimalField(
        max_digits=9 + 2,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(0))],
        verbose_name=_("amount"),
    )

    currency = models.CharField(
        max_length=3,
        choices=Currency.get_choices,
        default=Currency.EUR,
        verbose_name=_("currency"),
    )

    start_date = models.DateField(
        default=now,
        verbose_name=_("start date"),
    )

    class Frequency(models.TextChoices):  # pylint: disable=too-many-ancestors
        """Frequency choices."""

        WEEKLY = "W", _("weekly")
        MONTHLY = "M", _("monthly")
        YEARLY = "Y", _("yearly")

    frequency = models.CharField(
        max_length=1,
        choices=Frequency,
        default=Frequency.MONTHLY,
        verbose_name=_("frequency"),
    )

    occurrences = models.PositiveSmallIntegerField(  # 0 to 32767
        default=0,
        verbose_name=_("occurrences"),
        help_text=_("Zero for perpetual repetition."),
    )

    occurrence_range = models.PositiveSmallIntegerField(  # 1 to 32767
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("occurrence range"),
    )

    # until (date)

    # toutes les x semaines le lundi
    # tous les x mois le 10
    # tous les x mois, le dernier jour (28, 29, 30, 31)
    # tous les x années le 10 juillet
    # tous les mois, le deuxième samedi

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["id"]
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        return self.title

    def get_events(self, start_date: date, end_date: date) -> list[Entry]:
        """Calcule les évènements sur une période comprise entre 'start_date' (inclue)
        et 'end_date' (exclue)."""
        del start_date, end_date
        return []
