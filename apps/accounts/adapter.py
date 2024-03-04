"""Adapter definitions for the 'accounts' application."""

from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest


class CustomUserAccountAdapter(DefaultAccountAdapter):
    """Adapter to enable or disable allauth new signups"""

    def is_open_for_signup(self, request: HttpRequest) -> bool:
        """Checks whether or not the site is open for signups."""
        current_site = get_current_site(request)
        return current_site.sitecustomization.is_open_for_signup
