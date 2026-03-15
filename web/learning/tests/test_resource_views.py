import pytest
from django.urls import reverse
from model_bakery import baker

from learning.models import LearningResource

pytestmark = pytest.mark.django_db


def test_resource_list_shows_user_resources(client_logged_in, user):
    resource = baker.make(LearningResource, user=user)
    baker.make(LearningResource)

    url = reverse("resources:resource_list")
    response = client_logged_in.get(url)

    assert response.status_code == 200
    assert resource in response.context["resources"]
    assert len(response.context["resources"]) == 1


def test_resource_detail_view(client_logged_in, user):
    resource = baker.make(LearningResource, user=user)

    url = reverse("resources:resource_detail", args=[resource.pk])
    response = client_logged_in.get(url)

    assert response.status_code == 200
    assert response.context["resource"] == resource


def test_resource_create(client_logged_in, user):
    url = reverse("resources:resource_create")

    data = {
        "title": "New Learning Resource",
        "resource_type": "udemy",
        "description": "A great course",
    }

    response = client_logged_in.post(url, data)

    assert response.status_code == 302
    assert LearningResource.objects.filter(
        title="New Learning Resource", user=user
    ).exists()


def test_resource_update(client_logged_in, user):
    resource = baker.make(
        LearningResource,
        user=user,
        title="Old Title",
        resource_type="book",
    )

    url = reverse("resources:resource_update", args=[resource.pk])

    data = {
        "title": "Updated Title",
        "resource_type": "book",
        "description": "",
    }

    response = client_logged_in.post(url, data)

    resource.refresh_from_db()

    assert response.status_code == 302
    assert resource.title == "Updated Title"


def test_resource_delete(client_logged_in, user):
    resource = baker.make(LearningResource, user=user)

    url = reverse("resources:resource_delete", args=[resource.pk])

    response = client_logged_in.post(url)

    assert response.status_code == 302
    assert not LearningResource.objects.filter(pk=resource.pk).exists()


def test_user_cannot_access_other_users_resource(client_logged_in):
    other_resource = baker.make(LearningResource)

    url = reverse("resources:resource_detail", args=[other_resource.pk])

    response = client_logged_in.get(url)

    assert response.status_code == 404


def test_user_cannot_update_other_users_resource(client_logged_in):
    other_resource = baker.make(LearningResource)

    url = reverse("resources:resource_update", args=[other_resource.pk])
    response = client_logged_in.post(url, {"title": "Hacked", "resource_type": "book"})

    assert response.status_code == 404


def test_user_cannot_delete_other_users_resource(client_logged_in):
    other_resource = baker.make(LearningResource)

    url = reverse("resources:resource_delete", args=[other_resource.pk])
    response = client_logged_in.post(url)

    assert response.status_code == 404


@pytest.mark.parametrize(
    "url",
    [
        lambda: reverse("resources:resource_list"),
        lambda: reverse("resources:resource_create"),
        lambda: reverse("resources:resource_detail", args=[999]),
        lambda: reverse("resources:resource_update", args=[999]),
        lambda: reverse("resources:resource_delete", args=[999]),
    ],
)
def test_resource_views_require_login(client, url):
    response = client.get(url())

    assert response.status_code == 302
    assert "/login/" in response.url
