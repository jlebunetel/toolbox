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
            "date_joined",
            "is_staff",
            "is_superuser",
            "first_name",
            "last_name",
        ]

    username = CharField(disabled=True)
    is_staff = BooleanField(disabled=True)
    is_superuser = BooleanField(disabled=True)
    date_joined = DateTimeField(disabled=True)


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
