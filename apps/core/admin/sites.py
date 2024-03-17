"""Configuration of the 'core' application administration site."""

from core.models import SiteCustomization
from django.contrib import admin
from django.contrib.sites.models import Site


class SiteAdmin(admin.ModelAdmin):
    """Encapsulate all admin options and functionality for the model 'Site'."""


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)


class SiteCustomizationAdmin(admin.ModelAdmin):
    """Encapsulate all admin options and functionality for the model
    'SiteCustomization'."""


admin.site.register(SiteCustomization, SiteCustomizationAdmin)
