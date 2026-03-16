from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from learning.forms import LearningUnitForm
from learning.models import LearningResource, LearningUnit


class UserResourceMixin(LoginRequiredMixin):
    """
    Ensures the resource belongs to the logged-in user.
    """

    def get_resource(self):
        return get_object_or_404(
            LearningResource,
            pk=self.kwargs["resource_pk"],
            user=self.request.user,
        )


class LearningUnitCreateView(UserResourceMixin, CreateView):
    """
    Create a learning unit within a resource.
    """

    model = LearningUnit
    form_class = LearningUnitForm
    template_name = "units/unit_form.html"

    def form_valid(self, form):
        resource = self.get_resource()
        form.instance.resource = resource
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "resources:resource_detail",
            kwargs={"pk": self.kwargs["resource_pk"]},
        )


class LearningUnitUpdateView(UserResourceMixin, UpdateView):
    """
    Update an existing learning unit.
    """

    model = LearningUnit
    form_class = LearningUnitForm
    template_name = "units/unit_form.html"
    pk_url_kwarg = "unit_pk"

    def get_queryset(self):
        resource = self.get_resource()
        return LearningUnit.objects.filter(resource=resource)

    def get_success_url(self):
        return reverse(
            "resources:resource_detail",
            kwargs={"pk": self.kwargs["resource_pk"]},
        )


class LearningUnitDeleteView(UserResourceMixin, DeleteView):
    """
    Delete a learning unit.
    """

    model = LearningUnit
    template_name = "units/unit_confirm_delete.html"
    pk_url_kwarg = "unit_pk"

    def get_queryset(self):
        resource = self.get_resource()
        return LearningUnit.objects.filter(resource=resource)

    def get_success_url(self):
        return reverse(
            "resources:resource_detail",
            kwargs={"pk": self.kwargs["resource_pk"]},
        )
