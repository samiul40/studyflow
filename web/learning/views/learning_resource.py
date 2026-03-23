from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from learning.forms import LearningResourceForm
from learning.mixins import UserPermissionMixin
from learning.models import LearningResource
from learning.services import get_resource_progress


class UserResourceMixin:
    """
    Restrict queryset to resources belonging to the logged-in user.
    """

    def get_queryset(self):
        return LearningResource.objects.filter(user=self.request.user).select_related(
            "user"
        )


class ResourceListView(UserPermissionMixin, UserResourceMixin, ListView):
    """
    Display all learning resources belonging to the logged-in user.
    """

    permission_required = "learning.view_learningresource"
    model = LearningResource
    template_name = "resources/resource_list.html"
    context_object_name = "resources"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search", "").strip()

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class ResourceDetailView(UserPermissionMixin, UserResourceMixin, DetailView):
    """
    Display details of a single learning resource.
    """

    permission_required = "learning.view_learningresource"
    model = LearningResource
    template_name = "resources/resource_detail.html"
    context_object_name = "resource"

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
    success_url = reverse_lazy("learning:resource_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Resource created successfully.")
        return super().form_valid(form)


class ResourceUpdateView(UserPermissionMixin, UserResourceMixin, UpdateView):
    """
    Update an existing learning resource belonging to the user.
    """

    permission_required = "learning.change_learningresource"
    model = LearningResource
    form_class = LearningResourceForm
    template_name = "resources/resource_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Resource updated successfully.")
        return super().form_valid(form)


class ResourceDeleteView(UserPermissionMixin, UserResourceMixin, DeleteView):
    """
    Delete a learning resource belonging to the user.
    """

    permission_required = "learning.delete_learningresource"
    model = LearningResource
    template_name = "resources/resource_confirm_delete.html"
    success_url = reverse_lazy("learning:resource_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Resource deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Resource deleted successfully.")
        return super().form_valid(form)
