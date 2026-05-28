import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

DASHBOARD_URL = reverse("learning:dashboard")


def test_dashboard_redirects_unauthenticated(client):
    response = client.get(DASHBOARD_URL)

    assert response.status_code == 302
    assert "/login/" in response.url


def test_dashboard_returns_200_for_authenticated_user(client_logged_in):
    response = client_logged_in.get(DASHBOARD_URL)

    assert response.status_code == 200


def test_dashboard_passes_type_filter_to_context(client_logged_in):
    response = client_logged_in.get(DASHBOARD_URL + "?type=book")

    assert response.status_code == 200
    assert response.context["active_filter"] == "book"


def test_dashboard_active_filter_is_none_without_query_param(client_logged_in):
    response = client_logged_in.get(DASHBOARD_URL)

    assert response.context["active_filter"] is None
