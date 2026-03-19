from django.urls import path

from .views import (
    LearningUnitCreateView,
    LearningUnitDeleteView,
    LearningUnitReorderView,
    LearningUnitToggleStatusView,
    LearningUnitUpdateView,
    ResourceCreateView,
    ResourceDeleteView,
    ResourceDetailView,
    ResourceListView,
    ResourceUpdateView,
    dashboard_view,
)

app_name = "learning"

urlpatterns = [
    path("", ResourceListView.as_view(), name="resource_list"),
    path("<int:pk>/", ResourceDetailView.as_view(), name="resource_detail"),
    path("create/", ResourceCreateView.as_view(), name="resource_create"),
    path("<int:pk>/edit/", ResourceUpdateView.as_view(), name="resource_update"),
    path("<int:pk>/delete/", ResourceDeleteView.as_view(), name="resource_delete"),
    path(
        "<int:resource_pk>/units/add/",
        LearningUnitCreateView.as_view(),
        name="unit_create",
    ),
    path(
        "<int:resource_pk>/units/<int:unit_pk>/edit/",
        LearningUnitUpdateView.as_view(),
        name="unit_update",
    ),
    path(
        "<int:resource_pk>/units/<int:unit_pk>/delete/",
        LearningUnitDeleteView.as_view(),
        name="unit_delete",
    ),
    path(
        "<int:resource_pk>/units/reorder/",
        LearningUnitReorderView.as_view(),
        name="unit_reorder",
    ),
    path(
        "units/<int:pk>/toggle-status/",
        LearningUnitToggleStatusView.as_view(),
        name="unit_toggle_status",
    ),
    path("dashboard/", dashboard_view, name="dashboard"),
]
