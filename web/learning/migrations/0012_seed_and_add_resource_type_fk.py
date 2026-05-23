import django.db.models.deletion
from django.db import migrations, models

SYSTEM_TYPES = [
    {"name": "YouTube", "slug": "youtube", "content_kind": "video"},
    {"name": "Udemy", "slug": "udemy", "content_kind": "video"},
    {"name": "Book", "slug": "book", "content_kind": "reading"},
    {"name": "Other", "slug": "other", "content_kind": "video"},
]

LEGACY_TO_SLUG = {
    "youtube": "youtube",
    "udemy": "udemy",
    "book": "book",
    "other": "other",
}


def seed_and_populate(apps, schema_editor):
    ResourceType = apps.get_model("learning", "ResourceType")
    LearningResource = apps.get_model("learning", "LearningResource")

    for data in SYSTEM_TYPES:
        ResourceType.objects.get_or_create(
            slug=data["slug"],
            defaults={
                "name": data["name"],
                "content_kind": data["content_kind"],
                "is_system": True,
            },
        )

    fallback = ResourceType.objects.get(slug="other")

    for resource in LearningResource.objects.all():
        slug = LEGACY_TO_SLUG.get(resource.resource_type_legacy, "other")
        rt = ResourceType.objects.filter(slug=slug).first() or fallback
        resource.resource_type_new = rt
        resource.save(update_fields=["resource_type_new"])


def reverse_populate(apps, schema_editor):
    LearningResource = apps.get_model("learning", "LearningResource")

    for resource in LearningResource.objects.select_related(
        "resource_type_new"
    ).all():
        if resource.resource_type_new:
            resource.resource_type_legacy = resource.resource_type_new.slug
            resource.save(update_fields=["resource_type_legacy"])


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0011_create_resource_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="learningresource",
            old_name="resource_type",
            new_name="resource_type_legacy",
        ),
        migrations.AddField(
            model_name="learningresource",
            name="resource_type_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="resources",
                to="learning.resourcetype",
            ),
        ),
        migrations.RunPython(seed_and_populate, reverse_populate),
    ]
