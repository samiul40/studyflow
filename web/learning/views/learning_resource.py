from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from learning.forms import LearningResourceForm
from learning.mixins import UserPermissionMixin
from learning.models import LearningResource, LearningUnit
from learning.services import get_resource_progress


class BaseUserResourceView(UserPermissionMixin):
    """
    Base view for learning resource views that restricts the queryset
    to resources owned by the currently authenticated user.
    """

    model = LearningResource

    def get_queryset(self):
        return LearningResource.objects.for_user(self.request.user).order_by(
            "-created_at"
        )


class ResourceListView(BaseUserResourceView, ListView):
    """
    Display all learning resources belonging to the logged-in user.
    """

    permission_required = "learning.view_learningresource"
    template_name = "resources/resource_list.html"
    context_object_name = "resources"

    def get_queryset(self):
        qs = super().get_queryset().with_progress().select_related("user")

        search_query = self.request.GET.get("search", "").strip()

        if search_query:
            qs = qs.filter(title__icontains=search_query)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class ResourceDetailView(BaseUserResourceView, DetailView):
    """
    Display details of a single learning resource.
    """

    permission_required = "learning.view_learningresource"
    template_name = "resources/resource_detail.html"
    context_object_name = "resource"

    def get_queryset(self):
        return super().get_queryset().with_progress()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        progress = get_resource_progress(self.object)
        context.update(progress)
        return context


class ResourceCreateView(UserPermissionMixin, CreateView):
    """
    Create a new learning resource.
    """

    permission_required = "learning.add_learningresource"
    model = LearningResource
    form_class = LearningResourceForm
    template_name = "resources/resource_form.html"

    def get_success_url(self):
        return reverse("learning:resource_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user

        response = super().form_valid(form)

        unit_count = form.cleaned_data.get("unit_count")

        if unit_count:
            name_map = {
                "book": "Chapter",
                "udemy": "Section",
                "youtube": "Video",
            }

            unit_label = name_map.get(self.object.resource_type, "Unit")

            units = [
                LearningUnit(
                    resource=self.object,
                    title=f"{unit_label} {i + 1}",
                    order=i + 1,
                )
                for i in range(unit_count)
            ]

            LearningUnit.objects.bulk_create(units)

        messages.success(self.request, "Resource created successfully.")
        return response


class ResourceUpdateView(BaseUserResourceView, UpdateView):
    """
    Update an existing learning resource belonging to the user.
    """

    permission_required = "learning.change_learningresource"
    form_class = LearningResourceForm
    template_name = "resources/resource_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Resource updated successfully.")
        return super().form_valid(form)


class ResourceDeleteView(BaseUserResourceView, DeleteView):
    """
    Delete a learning resource belonging to the user.
    """

    permission_required = "learning.delete_learningresource"
    model = LearningResource
    template_name = "resources/resource_confirm_delete.html"
    success_url = reverse_lazy("learning:resource_list")

    def form_valid(self, form):
        messages.success(self.request, "Resource deleted successfully.")
        return super().form_valid(form)
