import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

INDEX_URL = reverse("index")


def test_index_redirects_unauthenticated(client):
    response = client.get(INDEX_URL)

    assert response.status_code == 302
    assert "/login/" in response.url


def test_index_returns_200_for_authenticated_user(client_logged_in):
    response = client_logged_in.get(INDEX_URL)

    assert response.status_code == 200
