from django.db import models

from .learning_resource import LearningResource


class LearningUnit(models.Model):
    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    resource = models.ForeignKey(
        LearningResource,
        on_delete=models.CASCADE,
        related_name="units",
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_started",
    )
    video_progress_minutes = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    status__in=["not_started", "in_progress", "completed"]
                ),
                name="chk_status_valid",
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.resource.title})"

    def save(self, *args, **kwargs):
        if self.order is None:
            last_unit = (
                LearningUnit.objects.filter(resource=self.resource)
                .order_by("-order")
                .first()
            )

            self.order = 1 if not last_unit else last_unit.order + 1

        super().save(*args, **kwargs)
