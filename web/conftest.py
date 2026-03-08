import pytest
from model_bakery import baker


@pytest.fixture
def user(db):
    user = baker.make(
        "auth.User", username="testuser", is_superuser=True, is_staff=True
    )
    user.set_password("12345")
    user.save()
    return user


@pytest.fixture
def client_logged_in(client, user):
    client.force_login(user)
    return client
