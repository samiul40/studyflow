import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker

from learning.models import LearningResource, LearningUnit

pytestmark = pytest.mark.django_db


@pytest.fixture
def resource(user):
    return baker.make(LearningResource, user=user)


class TestLearningUnitStr:
    """Tests string representation of a learning unit."""

    def test_learning_unit_str(self, resource):
        unit = baker.make(LearningUnit, resource=resource, title="Lesson 1")
        assert str(unit) == f"Lesson 1 ({resource.title})"


class TestLearningUnitProgress:
    """Tests progress percentage calculations."""

    def test_progress_percent_no_data(self, resource):
        unit = baker.make(LearningUnit, resource=resource)
        assert unit.progress_percent == 0

    def test_progress_percent_partial(self, resource):
        unit = baker.make(
            LearningUnit,
            resource=resource,
            duration_minutes=100,
            video_progress_minutes=25,
        )
        assert unit.progress_percent == 25

    def test_progress_percent_full(self, resource):
        unit = baker.make(
            LearningUnit,
            resource=resource,
            duration_minutes=100,
            video_progress_minutes=100,
        )
        assert unit.progress_percent == 100


class TestLearningUnitStatus:
    """Tests status-related properties."""

    def test_is_status_locked_true(self, resource):
        unit = baker.make(
            LearningUnit,
            resource=resource,
            video_progress_minutes=10,
        )
        assert unit.is_status_locked is True

    def test_is_status_locked_false(self, resource):
        unit = baker.make(
            LearningUnit,
            resource=resource,
            video_progress_minutes=None,
        )
        assert unit.is_status_locked is False


class TestLearningUnitValidation:
    """Tests validation rules for learning units."""

    def test_progress_cannot_exceed_duration(self, resource):
        unit = LearningUnit(
            resource=resource,
            title="Test",
            duration_minutes=10,
            video_progress_minutes=20,
        )

        with pytest.raises(ValidationError):
            unit.full_clean()


class TestLearningUnitSave:
    """Tests automatic behaviour during save operations."""

    def test_order_auto_increment(self, resource):
        baker.make(LearningUnit, resource=resource, order=1)
        baker.make(LearningUnit, resource=resource, order=2)

        u3 = LearningUnit(resource=resource, title="New Unit")
        u3.save()

        assert u3.order == 3

    def test_status_not_started(self, resource):
        unit = LearningUnit(
            resource=resource,
            title="Test",
            duration_minutes=100,
            video_progress_minutes=0,
        )
        unit.save()

        assert unit.status == LearningUnit.StatusChoices.NOT_STARTED

    def test_status_in_progress(self, resource):
        unit = LearningUnit(
            resource=resource,
            title="Test",
            duration_minutes=100,
            video_progress_minutes=50,
        )
        unit.save()

        assert unit.status == LearningUnit.StatusChoices.IN_PROGRESS

    def test_status_completed(self, resource):
        unit = LearningUnit(
            resource=resource,
            title="Test",
            duration_minutes=100,
            video_progress_minutes=100,
        )
        unit.save()

        assert unit.status == LearningUnit.StatusChoices.COMPLETED

    def test_status_not_updated_when_progress_none(self, resource):
        unit = LearningUnit(
            resource=resource,
            title="Test",
            duration_minutes=100,
            video_progress_minutes=None,
            status=LearningUnit.StatusChoices.IN_PROGRESS,
        )
        unit.save()

        assert unit.status == LearningUnit.StatusChoices.IN_PROGRESS
