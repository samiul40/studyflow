import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, IntegerField, Max, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
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


class UserUnitMixin(LoginRequiredMixin):
    """
    Ensures the learning unit belongs to the logged-in user.
    """

    def get_unit(self):
        return get_object_or_404(
            LearningUnit,
            pk=self.kwargs["pk"],
            resource__user=self.request.user,
        )


class ResourceRedirectMixin:
    """
    Redirects to the parent resource detail page after a successful action.
    """

    def get_success_url(self):
        return reverse(
            "learning:resource_detail",
            kwargs={"pk": self.kwargs["resource_pk"]},
        )


class LearningUnitCreateView(UserResourceMixin, ResourceRedirectMixin, CreateView):
    """
    Create a learning unit within a resource.
    """

    model = LearningUnit
    form_class = LearningUnitForm

    def form_valid(self, form):
        resource = self.get_resource()
        form.instance.resource = resource
        return super().form_valid(form)


class LearningUnitBulkCreateView(UserResourceMixin, View):
    def post(self, request, *args, **kwargs):
        resource = self.get_resource()

        titles = request.POST.getlist("title[]")
        durations = request.POST.getlist("duration[]")

        last_order = (
            LearningUnit.objects.filter(resource=resource).aggregate(
                max_order=Max("order")
            )["max_order"]
            or 0
        )

        new_units = []

        for index, (title, duration) in enumerate(zip(titles, durations), start=1):
            if not title.strip():
                continue

            new_units.append(
                LearningUnit(
                    resource=resource,
                    title=title.strip(),
                    duration_minutes=int(duration) if duration else 0,
                    order=last_order + index,
                )
            )

        LearningUnit.objects.bulk_create(new_units)

        return redirect(resource.get_absolute_url())


class LearningUnitUpdateView(UserResourceMixin, ResourceRedirectMixin, UpdateView):
    """
    Update an existing learning unit.
    """

    model = LearningUnit
    form_class = LearningUnitForm
    pk_url_kwarg = "unit_pk"

    def get_queryset(self):
        resource = self.get_resource()
        return LearningUnit.objects.filter(resource=resource)


class LearningUnitDeleteView(UserResourceMixin, ResourceRedirectMixin, DeleteView):
    """
    Delete a learning unit.
    """

    model = LearningUnit
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


class LearningUnitReorderView(UserResourceMixin, View):
    """
    Update learning unit order after drag-and-drop.
    """

    def post(self, request, resource_pk):
        resource = self.get_resource()
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


class LearningUnitUpdateStatusView(UserUnitMixin, View):
    def post(self, request, pk):
        unit = self.get_unit()

        new_status = request.POST.get("status")

        if (
            new_status in ["not_started", "in_progress", "completed"]
            and unit.status != new_status
        ):
            unit.status = new_status
            unit.save()

        return redirect(unit.resource.get_absolute_url())
