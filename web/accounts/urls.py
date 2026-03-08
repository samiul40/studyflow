# Django
from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.logout, name="logout"),
    path("settings/", views.settings, name="settings"),
    path("profile/", views.profile, name="profile"),
]