"""Generic admin mixins."""

from core.models.mixins import SensitiveMixin
from django.contrib import admin


class SensitiveAdminMixin(admin.ModelAdmin):
    """Mixin to enhance the security on sensitive models."""

    def save_model(self, request, obj, form, change):
        """Given a model instance save it to the database."""
        obj.changed_by = request.user
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Given the 'HttpRequest', the parent 'ModelForm' instance, the
        list of inline formsets and a boolean value based on whether the
        parent is being added or changed, save the related objects to the
        database. Note that at this point save_form() and save_model() have
        already been called.
        """
        for formset in formsets:
            if issubclass(formset.model, SensitiveMixin):
                instances = formset.save(commit=False)

                for instance in instances:
                    instance.changed_by = request.user

                for added_obj in formset.new_objects:
                    added_obj.created_by = request.user

                for deleted_obj in formset.deleted_objects:
                    del deleted_obj

                for changed_obj in formset.changed_objects:
                    del changed_obj

        super().save_related(request, form, formsets, change)
