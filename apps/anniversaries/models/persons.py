"""Model definitions for the 'anniversaries' application."""

import logging
from datetime import date
from uuid import uuid4

from anniversaries.utils import IEvent, get_anniversary_list, get_ievent, get_ievent_uid
from core.models.mixins import SensitiveMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.template.defaultfilters import date as format_date
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from .families import Family

NAMES_MAX_LENGHT: int = 255

logger = logging.getLogger(__name__)


class Person(SensitiveMixin, models.Model):
    """Class to represent someone."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    nickname = models.CharField(
        max_length=NAMES_MAX_LENGHT,
        blank=True,
        verbose_name=_("nickname"),
    )

    first_name = models.CharField(
        max_length=NAMES_MAX_LENGHT,
        verbose_name=_("first name"),
    )

    middle_names = ArrayField(
        base_field=models.CharField(
            max_length=NAMES_MAX_LENGHT,
            blank=True,
        ),
        blank=True,
        verbose_name=_("middle names"),
        help_text=_("Middle names separated by commas."),
    )

    birth_name = models.CharField(
        max_length=NAMES_MAX_LENGHT,
        blank=True,
        verbose_name=_("birth name"),
    )

    married_name = models.CharField(
        max_length=NAMES_MAX_LENGHT,
        blank=True,
        verbose_name=_("married name"),
    )

    preferred_name = models.CharField(
        max_length=NAMES_MAX_LENGHT,
        blank=True,
        verbose_name=_("preferred name"),
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("date of birth"),
    )

    date_of_death = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("date of death"),
    )

    SEX_UNKNOWN = 0
    SEX_MALE = 1
    SEX_FEMALE = 2

    SEX_CHOICES = [
        (SEX_UNKNOWN, _("🧒 unknown")),
        (SEX_MALE, _("👦 male")),
        (SEX_FEMALE, _("👧 female")),
    ]

    sex = models.PositiveSmallIntegerField(
        choices=SEX_CHOICES,
        default=SEX_UNKNOWN,
        verbose_name=_("sex"),
    )

    SPECIES_UNKNOWN = 0
    SPECIES_HUMAN = 1
    SPECIES_CAT = 2
    SPECIES_DOG = 3

    SPECIES_CHOICES = [
        (SPECIES_UNKNOWN, _("🦄 unknown")),
        (SPECIES_HUMAN, _("🧒 human")),
        (SPECIES_CAT, _("🐱 cat")),
        (SPECIES_DOG, _("🐶 dog")),
    ]

    species = models.PositiveSmallIntegerField(
        choices=SPECIES_CHOICES,
        default=SPECIES_HUMAN,
        verbose_name=_("species"),
    )

    families = models.ManyToManyField(  # type: ignore
        to=Family,
        related_name="anniversaries_family_members",
        related_query_name="anniversaries_family_member",
        verbose_name=_("families"),
    )

    class Meta(SensitiveMixin.Meta):
        """Metadata options class."""

        ordering: list[str] = ["-date_of_birth"]
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def __repr__(self) -> str:
        """Returns an unambiguous description of the model (for developers)."""
        return f"<{self.__class__.__name__} object ({self.pk})>"

    def __str__(self) -> str:
        """Returns a description of the model (for customers)."""
        is_dead: str = "🪦" if self.date_of_death else ""
        emoji: str = self.get_emoji()
        return " ".join([emoji, self.full_name, is_dead]).strip()

    @property
    def last_name(self) -> str:
        """Returns the last name of the model."""
        return self.preferred_name or self.married_name or self.birth_name

    @property
    def full_name(self) -> str:
        """Returns the full name of the model."""
        return " ".join([self.first_name, self.last_name]).strip()

    @property
    def short_name(self) -> str:
        """Returns the short name of the model."""
        return self.nickname or self.first_name

    def get_emoji(self) -> str:  # noqa: R901
        """Returns an iconic representation of the model."""
        match self.species:
            case self.SPECIES_UNKNOWN:
                return "🦄"
            case self.SPECIES_CAT:
                return "🐱"
            case self.SPECIES_DOG:
                return "🐶"
            case _:
                pass

        age = self.get_current_age()
        if not age:
            return "🧒"

        match age < 3, age < 18, age < 60, self.sex:
            case True, _, _, _:
                emoji = "👶"
            case _, True, _, self.SEX_MALE:
                emoji = "👦"
            case _, True, _, self.SEX_FEMALE:
                emoji = "👧"
            case _, True, _, _:
                emoji = "🧒"
            case _, _, True, self.SEX_MALE:
                emoji = "👨"
            case _, _, True, self.SEX_FEMALE:
                emoji = "👩"
            case _, _, True, _:
                emoji = "🧑"
            case _, _, _, self.SEX_MALE:
                emoji = "👴"
            case _, _, _, self.SEX_MALE:
                emoji = "👵"
            case _, _, _, _:
                emoji = "🧓"

        return emoji

    def get_current_age(self) -> int | None:
        """Returns the current age of the model or None."""
        if not self.date_of_birth:
            return None

        return len(
            get_anniversary_list(
                event_date=self.date_of_birth,
                end_date=self.date_of_death or date.today(),
            )
        )

    def get_birthday_list(self, end_date: date = date.today()) -> list[date]:
        """Returns the list of birthdays (including the date of birth)."""
        if not self.date_of_birth:
            return []

        return [self.date_of_birth] + get_anniversary_list(
            event_date=self.date_of_birth,
            end_date=self.date_of_death or end_date,
        )

    def get_birthday_ievent_summary(self, age: int) -> str:
        """Returns a simple description in the context of a birthday."""
        if age == 0:
            return "🎉 " + _("Birth of %(name)s") % {"name": self.short_name}
        age_display: str = ngettext_lazy(
            "%(age)d year",
            "%(age)d years",
            "age",
        ) % {"age": age}
        return f"🎂 {self.short_name} ({age_display})"

    def get_birthday_ievent_description(self, age: int) -> str:
        """Returns a more complete description in the context of a birthday."""
        if age == 0:
            return _("%(name)s was born today.") % {"name": self.full_name}

        return ", ".join(
            [
                _("%(name)s was born on %(date)s")
                % {
                    "name": self.full_name,
                    "date": format_date(self.date_of_birth),
                },
                ngettext_lazy(
                    "one year ago.",
                    "%(age)d years ago.",
                    "age",
                )
                % {"age": age},
            ]
        )

    def get_birthday_ievent_list(self, end_date: date = date.today()) -> list[IEvent]:
        """Returns the list of birthdays (including the date of birth) as
        icalendar.Event list."""
        ievents: list[IEvent] = []
        for age, event_date in enumerate(self.get_birthday_list(end_date=end_date)):
            ievents.append(
                get_ievent(
                    envent_date=event_date,
                    uid=get_ievent_uid(
                        root=str(self.id), context="birthday", index=age
                    ),
                    summary=self.get_birthday_ievent_summary(age=age),
                    description=self.get_birthday_ievent_description(age=age),
                )
            )
        return ievents

    def get_death_anniversary_list(self, end_date: date = date.today()) -> list[date]:
        """Returns the list of death anniversaries (including the date of death)."""
        if not self.date_of_death:
            return []

        return [self.date_of_death] + get_anniversary_list(
            event_date=self.date_of_death,
            end_date=end_date,
        )

    def get_death_anniversary_ievent_summary(self, age: int) -> str:
        """Returns a simple description in the context of a death anniversary."""
        if age == 0:
            return "🪦 " + _("Death of %(name)s") % {"name": self.short_name}
        age_display: str = ngettext_lazy(
            "%(age)d year",
            "%(age)d years",
            "age",
        ) % {"age": age}
        return f"🪦 {self.short_name} ({age_display})"

    def get_death_anniversary_ievent_description(self, age: int) -> str:
        """Returns a more complete description in the context of a death anniversary."""
        if age == 0:
            return _("%(name)s died today.") % {"name": self.full_name}

        return ", ".join(
            [
                _("%(name)s died on %(date)s")
                % {
                    "name": self.full_name,
                    "date": format_date(self.date_of_death),
                },
                ngettext_lazy(
                    "one year ago.",
                    "%(age)d years ago.",
                    "age",
                )
                % {"age": age},
            ]
        )

    def get_death_anniversary_ievent_list(
        self, end_date: date = date.today()
    ) -> list[IEvent]:
        """Returns the list of death anniversaries (including the date of death)
        as icalendar.Event list."""
        ievents: list[IEvent] = []
        for age, event_date in enumerate(
            self.get_death_anniversary_list(end_date=end_date)
        ):
            ievents.append(
                get_ievent(
                    envent_date=event_date,
                    uid=get_ievent_uid(root=str(self.id), context="death", index=age),
                    summary=self.get_death_anniversary_ievent_summary(age=age),
                    description=self.get_death_anniversary_ievent_description(age=age),
                )
            )
        return ievents
