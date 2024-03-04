"""Register 'core' actions with 'manage.py'."""

from accounts.models import User
from allauth.account.models import EmailAddress
from core.models import SiteCustomization
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError


def update_or_create_default_site(
    *, site_id: int, domain: str, name: str
) -> tuple[Site, bool]:
    """Update the site with default values if it exists, creates it otherwise."""
    site, created = Site.objects.get_or_create(pk=site_id)
    site.domain = domain
    site.name = name
    site.save()
    SiteCustomization.objects.get_or_create(site=site)
    return site, created


def update_or_create_superuser(
    *, username: str, password: str, email: str
) -> tuple[User, bool]:
    """Update the superuser with default values if it exists, creates it otherwise."""
    user, created = User.objects.get_or_create(username=username)
    user.set_password(password)
    user.email = email
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.save()
    email_address, _ = EmailAddress.objects.get_or_create(user=user, email=email)
    email_address.verified = True
    email_address.primary = True
    email_address.save()
    return user, created


class Command(BaseCommand):
    """Command to customize the project with default settings."""

    help: str = "Customize the project"

    def handle(self, *args: str, **kwargs: int) -> None:
        """Updates or creates the default site configuration and superuser."""
        del args, kwargs
        try:
            site, created = update_or_create_default_site(
                site_id=settings.SITE_ID,
                domain=settings.CUSTOM_SITE_DOMAIN,
                name=settings.CUSTOM_SITE_NAME,
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully create site "{site}"')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully update site "{site}"')
                )
            user, created = update_or_create_superuser(
                username=settings.CUSTOM_SUPERUSER_USERNAME,
                password=settings.CUSTOM_SUPERUSER_PASSWORD,
                email=settings.CUSTOM_SUPERUSER_EMAIL,
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully create superuser "{user}"')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully update superuser "{user}"')
                )
        except Exception as error:
            raise CommandError(error) from error
