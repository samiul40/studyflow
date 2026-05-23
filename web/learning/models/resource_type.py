from django.db import models
from django.utils.text import slugify


class ResourceType(models.Model):
    class ContentKind(models.TextChoices):
        VIDEO = "video", "Video / Audio"
        READING = "reading", "Reading"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    content_kind = models.CharField(
        max_length=20,
        choices=ContentKind.choices,
        default=ContentKind.VIDEO,
    )
    is_system = models.BooleanField(
        default=False,
        help_text="System types are pre-seeded and cannot be deleted.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "resource_type"
        ordering = ["-is_system", "name"]

    def __str__(self):
        return self.name

    @property
    def unit_label(self):
        if self.content_kind == self.ContentKind.READING:
            return "Chapter"
        return "Unit"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
