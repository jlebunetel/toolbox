"""View definitions for the 'accounts' application."""

from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit the user profile."""

    model = User
    fields = ["first_name", "last_name"]
    template_name: str = "accounts/profile.html"
    success_message: str = _("Profile successfully changed.")

    def get_object(self, queryset=None) -> User:
        """Returns the current logged user."""
        del queryset
        return self.request.user
