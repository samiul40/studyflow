from django.db import models
from django.db.models import (
    Case,
    Count,
    ExpressionWrapper,
    F,
    IntegerField,
    Q,
    Value,
    When,
)


class LearningResourceQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)

    def with_progress(self):
        return self.annotate(
            total_units=Count("units"),
            completed_units=Count(
                "units",
                filter=Q(units__status="completed"),
            ),
        ).annotate(
            percentage=Case(
                When(total_units=0, then=Value(0)),
                default=ExpressionWrapper(
                    100.0 * F("completed_units") / F("total_units"),
                    output_field=IntegerField(),
                ),
            )
        )
