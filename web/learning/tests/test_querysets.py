import pytest
from model_bakery import baker

from learning.models import LearningResource

pytestmark = pytest.mark.django_db


class TestLearningResourceForUser:
    """Tests for filtering learning resources by user."""

    def test_for_user_returns_only_user_resources(self, user):
        other_user = baker.make("auth.User")

        r1 = baker.make(LearningResource, user=user)
        baker.make(LearningResource, user=other_user)

        results = LearningResource.objects.for_user(user)

        assert list(results) == [r1]


class TestLearningResourceWithProgress:
    """Tests for progress annotations on learning resources."""

    def test_with_progress_no_units(self, user):
        resource = baker.make(LearningResource, user=user)

        result = LearningResource.objects.with_progress().get(pk=resource.pk)

        assert result.total_units == 0
        assert result.completed_units == 0
        assert result.percentage == 0

    def test_with_progress_partial_completion(self, user):
        resource = baker.make(LearningResource, user=user)

        baker.make("learning.LearningUnit", resource=resource, status="completed")
        baker.make("learning.LearningUnit", resource=resource, status="completed")
        baker.make("learning.LearningUnit", resource=resource, status="in_progress")

        result = LearningResource.objects.with_progress().get(pk=resource.pk)

        assert result.total_units == 3
        assert result.completed_units == 2
        assert result.percentage == int((2 / 3) * 100)

    def test_with_progress_all_completed(self, user):
        resource = baker.make(LearningResource, user=user)

        baker.make(
            "learning.LearningUnit",
            resource=resource,
            status="completed",
            _quantity=3,
        )

        result = LearningResource.objects.with_progress().get(pk=resource.pk)

        assert result.total_units == 3
        assert result.completed_units == 3
        assert result.percentage == 100

    def test_with_progress_none_completed(self, user):
        resource = baker.make(LearningResource, user=user)

        baker.make(
            "learning.LearningUnit",
            resource=resource,
            status="not_started",
            _quantity=3,
        )

        result = LearningResource.objects.with_progress().get(pk=resource.pk)

        assert result.total_units == 3
        assert result.completed_units == 0
        assert result.percentage == 0
