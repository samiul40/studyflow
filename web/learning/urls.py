from django.urls import path

from .views import (
    ResourceCreate,
    ResourceDelete,
    ResourceDetail,
    ResourceList,
    ResourceUpdate,
)

app_name = "resources"

urlpatterns = [
    path("", ResourceList.as_view(), name="resource_list"),
    path("<int:pk>/", ResourceDetail.as_view(), name="resource_detail"),
    path("create/", ResourceCreate.as_view(), name="resource_create"),
    path("<int:pk>/edit/", ResourceUpdate.as_view(), name="resource_update"),
    path("<int:pk>/delete/", ResourceDelete.as_view(), name="resource_delete"),
]
