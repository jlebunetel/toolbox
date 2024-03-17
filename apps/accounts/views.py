"""View definitions for the 'accounts' application."""

from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BooleanField, CharField, DateTimeField, ModelForm
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView


class ProfileForm(ModelForm):
    """Form to edit the user profile."""

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "is_staff",
            "is_superuser",
        ]

    username = CharField(disabled=True, label=_("Username"))
    is_staff = BooleanField(
        disabled=True,
        label=_("Staff status"),
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = BooleanField(
        disabled=True,
        label=_("Superuser status"),
        help_text=_(
            "Designates that this user has all permissions without explicitly assigning"
            " them."
        ),
    )
    date_joined = DateTimeField(disabled=True, label=_("Date joined"))


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit the user profile."""

    model = User
    form_class = ProfileForm
    template_name: str = "accounts/profile.html"
    success_message: str = _("Profile successfully changed.")

    def get_object(self, queryset=None) -> User:
        """Returns the current logged user."""
        del queryset
        return self.request.user
