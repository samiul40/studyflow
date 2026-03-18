from django.conf import settings
from django.db import models
from django.urls import reverse


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

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def get_absolute_url(self):
        return reverse("learning:resource_detail", kwargs={"pk": self.pk})

    @property
    def completion_percentage(self):
        total = self.units.count()
        completed = self.units.filter(status="completed").count()
        return int((completed / total) * 100) if total > 0 else 0

    @property
    def total_units(self):
        return self.units.count()

    @property
    def completed_units(self):
        return self.units.filter(status="completed").count()

    @property
    def incomplete_units(self):
        return self.total_units - self.completed_units

    @property
    def status_label(self):
        if self.completion_percentage == 100:
            return "Completed"
        elif self.completion_percentage > 0:
            return "In Progress"
        return "Not Started"
