from django.conf import settings
from django.db import models


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
        db_index=True,
    )
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user.username}"
