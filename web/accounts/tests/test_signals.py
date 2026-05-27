import pytest
from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from model_bakery import baker

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_signup_assigns_learning_user_group():
    Group.objects.get_or_create(name="Learning User")
    user = baker.make(User)

    user_signed_up.send(sender=User, request=None, user=user)

    assert user.groups.filter(name="Learning User").exists()


def test_signup_creates_group_if_missing():
    Group.objects.filter(name="Learning User").delete()
    user = baker.make(User)

    user_signed_up.send(sender=User, request=None, user=user)

    assert user.groups.filter(name="Learning User").exists()
