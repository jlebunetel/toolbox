"""View definitions for the 'labbooks' application."""

import django_filters
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from labbooks.models import Note


class DashbordView(LoginRequiredMixin, TemplateView):
    """The labbooks dashboard view."""

    template_name: str = "labbooks/dashboard.html"


class NoteFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(lookup_expr="icontains", field_name="tags")
    body = django_filters.CharFilter(lookup_expr="icontains", field_name="body")

    class Meta:
        model = Note
        fields = ["tags", "body"]


class NoteListView(LoginRequiredMixin, FilterView):
    model = Note

    filterset_class = NoteFilter


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ["body"]
    object: Note

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save(False)
        self.object.changed_by = self.request.user
        self.object.created_by = self.request.user
        self.object.save()
        messages.success(self.request, _("Note created successfully!"))
        return HttpResponseRedirect(self.get_success_url())


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ["body"]
    object: Note
    template_name_suffix = "_update_form"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save(False)
        self.object.changed_by = self.request.user
        self.object.save()
        messages.success(self.request, _("Note saved successfully!"))
        return HttpResponseRedirect(self.get_success_url())


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("labbooks:note-list")
