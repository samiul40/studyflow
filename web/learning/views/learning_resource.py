from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from learning.forms import LearningResourceForm
from learning.models import LearningResource


@method_decorator(login_required, name="dispatch")
class ResourceList(View):
    def get(self, request):
        resources = LearningResource.objects.filter(user=request.user)
        return render(request, "resources/resource_list.html", {"resources": resources})


@method_decorator(login_required, name="dispatch")
class ResourceDetail(View):
    def get(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk, user=request.user)
        return render(request, "resources/resource_detail.html", {"resource": resource})


@method_decorator(login_required, name="dispatch")
class ResourceCreate(View):
    def get(self, request):
        form = LearningResourceForm()
        return render(request, "resources/resource_form.html", {"form": form})

    def post(self, request):
        form = LearningResourceForm(request.POST)
        if form.is_valid():
            resource = LearningResource.create_for_user(request.user, form)
            messages.success(request, "Resource created successfully")
            return redirect("resources:resource_detail", pk=resource.pk)
        return render(request, "resources/resource_form.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class ResourceUpdate(View):
    def get(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk, user=request.user)
        form = LearningResourceForm(instance=resource)
        return render(
            request,
            "resources/resource_form.html",
            {"form": form, "resource": resource},
        )

    def post(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk, user=request.user)
        form = LearningResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource updated successfully")
            return redirect("resources:resource_detail", pk=resource.pk)
        return render(
            request,
            "resources/resource_form.html",
            {"form": form, "resource": resource},
        )


@method_decorator(login_required, name="dispatch")
class ResourceDelete(View):
    def get(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk, user=request.user)
        return render(
            request, "resources/resource_confirm_delete.html", {"resource": resource}
        )

    def post(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk, user=request.user)
        resource.delete()
        messages.success(request, "Resource deleted successfully")
        return redirect("resources:resource_list")
