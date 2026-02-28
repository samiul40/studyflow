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
    order = models.PositiveIntegerField()
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
        unique_together = ("resource", "order")

    def __str__(self):
        return f"{self.title} ({self.resource.title})"
