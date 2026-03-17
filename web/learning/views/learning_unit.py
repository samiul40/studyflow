import json

from django.contrib.auth.mixins import LoginRequiredMixin

# import json
# from django.http import JsonResponse
# from django.views import View
from django.db.models import Case, IntegerField, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
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


class ResourceRedirectMixin:
    """
    Redirects to the parent resource detail page after a successful action.
    """

    def get_success_url(self):
        return reverse(
            "resources:resource_detail",
            kwargs={"pk": self.kwargs["resource_pk"]},
        )


class LearningUnitCreateView(UserResourceMixin, ResourceRedirectMixin, CreateView):
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


class LearningUnitUpdateView(UserResourceMixin, ResourceRedirectMixin, UpdateView):
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


class LearningUnitDeleteView(UserResourceMixin, ResourceRedirectMixin, DeleteView):
    """
    Delete a learning unit.
    """

    model = LearningUnit
    template_name = "units/unit_confirm_delete.html"
    pk_url_kwarg = "unit_pk"

    def get_queryset(self):
        resource = self.get_resource()
        return LearningUnit.objects.filter(resource=resource)

    def form_valid(self, form):
        unit = self.get_object()
        resource = unit.resource

        response = super().form_valid(form)

        units = list(LearningUnit.objects.filter(resource=resource).order_by("order"))

        for index, unit in enumerate(units, start=1):
            unit.order = index

        LearningUnit.objects.bulk_update(units, ["order"])

        return response


class LearningUnitReorderView(LoginRequiredMixin, View):
    """
    Update learning unit order after drag-and-drop.
    """

    def post(self, request, resource_pk):

        resource = get_object_or_404(
            LearningResource,
            pk=resource_pk,
            user=request.user,
        )

        data = json.loads(request.body)

        cases = []
        ids = []

        for item in data["order"]:
            ids.append(item["id"])
            cases.append(When(id=item["id"], then=item["order"]))

        LearningUnit.objects.filter(resource=resource, id__in=ids).update(
            order=Case(*cases, output_field=IntegerField())
        )

        return JsonResponse({"status": "ok"})
