from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from learning.forms import LearningResourceForm
from learning.models import LearningResource


class UserResourceMixin:
    """
    Restrict queryset to resources belonging to the logged-in user.
    """

    def get_queryset(self):
        return LearningResource.objects.filter(user=self.request.user).select_related(
            "user"
        )


class ResourceListView(LoginRequiredMixin, UserResourceMixin, ListView):
    """
    Display all learning resources belonging to the logged-in user.
    """

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


class ResourceDetailView(LoginRequiredMixin, UserResourceMixin, DetailView):
    """
    Display details of a single learning resource.
    """

    model = LearningResource
    template_name = "resources/resource_detail.html"
    context_object_name = "resource"


class ResourceCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new learning resource.
    """

    model = LearningResource
    form_class = LearningResourceForm
    template_name = "resources/resource_form.html"
    success_url = reverse_lazy("learning:resource_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ResourceUpdateView(LoginRequiredMixin, UserResourceMixin, UpdateView):
    """
    Update an existing learning resource belonging to the user.
    """

    model = LearningResource
    form_class = LearningResourceForm
    template_name = "resources/resource_form.html"


class ResourceDeleteView(LoginRequiredMixin, UserResourceMixin, DeleteView):
    """
    Delete a learning resource belonging to the user.
    """

    model = LearningResource
    template_name = "resources/resource_confirm_delete.html"
    success_url = reverse_lazy("learning:resource_list")
