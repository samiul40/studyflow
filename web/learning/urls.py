from django.urls import path

from .views import (
    ResourceCreateView,
    ResourceDeleteView,
    ResourceDetailView,
    ResourceListView,
    ResourceUpdateView,
)

app_name = "resources"

urlpatterns = [
    path("", ResourceListView.as_view(), name="resource_list"),
    path("<int:pk>/", ResourceDetailView.as_view(), name="resource_detail"),
    path("create/", ResourceCreateView.as_view(), name="resource_create"),
    path("<int:pk>/edit/", ResourceUpdateView.as_view(), name="resource_update"),
    path("<int:pk>/delete/", ResourceDeleteView.as_view(), name="resource_delete"),
]
