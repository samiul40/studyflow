# Django
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_get_login_page(client):
    url = reverse("login")
    res = client.get(url)

    assert res.status_code == 200
    assert "Sign in" in res.content.decode()


def test_valid_login_redirects(client, user):
    url = reverse("login")
    res = client.post(url, {"username": user.username, "password": "12345"})

    assert res.status_code == 302
    assert res.url == reverse("learning:dashboard")


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


def test_settings_profile_update(client_logged_in, user):
    url = reverse("settings")
    res = client_logged_in.post(
        url,
        {
            "form_type": "profile",
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
        },
    )

    assert res.status_code == 302
    assert res.url == url
    user.refresh_from_db()
    assert user.first_name == "Alice"
    assert user.last_name == "Smith"
    assert user.email == "alice@example.com"


def test_settings_profile_update_duplicate_email(client_logged_in, user):
    other = User.objects.create_user(
        username="other", email="taken@example.com", password="pass"
    )
    url = reverse("settings")
    res = client_logged_in.post(
        url,
        {
            "form_type": "profile",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": other.email,
        },
    )

    assert res.status_code == 200
    assert b"already in use" in res.content


def test_settings_password_change(client_logged_in, user):
    url = reverse("settings")
    res = client_logged_in.post(
        url,
        {
            "form_type": "password",
            "old_password": "12345",
            "new_password1": "NewPass!99",
            "new_password2": "NewPass!99",
        },
    )

    assert res.status_code == 302
    assert res.url == url
    user.refresh_from_db()
    assert user.check_password("NewPass!99")


def test_settings_password_change_wrong_old(client_logged_in):
    url = reverse("settings")
    res = client_logged_in.post(
        url,
        {
            "form_type": "password",
            "old_password": "wrongpassword",
            "new_password1": "NewPass!99",
            "new_password2": "NewPass!99",
        },
    )

    assert res.status_code == 200
    assert b"old_password" in res.content or b"incorrect" in res.content.lower()
