# Django
from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.logout, name="logout"),
    path("settings/", views.Settings.as_view(), name="settings"),
]
