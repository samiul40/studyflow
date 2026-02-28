# Django
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

api_patterns = [
    path("learning/", include("learning.api.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_patterns)),
]


if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
