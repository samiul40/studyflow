from django.conf import settings
from django.db import models
from django.urls import reverse

from .querysets import LearningResourceQuerySet


class LearningResource(models.Model):
    RESOURCE_TYPES = [
        ("udemy", "Udemy"),
        ("book", "Book"),
        ("youtube", "YouTube"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_resources",
    )
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True, help_text="Optional link to the resource")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LearningResourceQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("view_dashboard", "Can view the dashboard with learning statistics"),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def get_absolute_url(self):
        return reverse("learning:resource_detail", kwargs={"pk": self.pk})
