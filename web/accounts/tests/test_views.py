# Django
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_get_login_page(client):
    url = reverse("login")
    res = client.get(url)

    assert res.status_code == 200
    assert "Login" in res.content.decode()


def test_valid_login_redirects(client, user):
    url = reverse("login")
    res = client.post(url, {"username": user.username, "password": "12345"})

    assert res.status_code == 302
    assert res.url == reverse("index")


def test_invalid_login(client, user):
    url = reverse("login")
    res = client.post(
        url,
        {"username": user.username, "password": "wrong"},
    )

    assert res.status_code == 302
    assert res.url == reverse("login")


def test_logout_redirects_to_login(client_logged_in):
    url = reverse("logout")
    res = client_logged_in.post(url)

    assert res.status_code == 302
    assert res.url == reverse("login")


def test_profile_view_requires_login(client):
    url = reverse("profile")
    res = client.get(url)

    assert res.status_code == 302  # Redirect to login
    assert reverse("login") in res.url


def test_profile_view_logged_in(client_logged_in):
    url = reverse("profile")
    res = client_logged_in.get(url)

    assert res.status_code == 200
    assert b"Welcome" in res.content or b"profile" in res.content.lower()


def test_settings_view_requires_login(client):
    url = reverse("settings")
    res = client.get(url)

    assert res.status_code == 302  # Redirect to login
    assert reverse("login") in res.url


def test_settings_view_logged_in(client_logged_in):
    url = reverse("settings")
    res = client_logged_in.get(url)

    assert res.status_code == 200
    assert b"Settings" in res.content or b"settings" in res.content.lower()
