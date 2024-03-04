"""Configuration of the 'accounts' application administration site."""

from accounts.models import User
from allauth.account.models import EmailAddress
from django.contrib.admin import TabularInline, site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.base import ModelBase


class EmailAddressInline(TabularInline):
    """Options for inline editing of 'User' instances."""

    model: ModelBase = EmailAddress
    extra: int = 0


class UserAdmin(BaseUserAdmin):
    """Encapsulate all admin options and functionality for the model 'User'."""

    readonly_fields = ("username",)
    inlines = [EmailAddressInline]


site.register(User, UserAdmin)
