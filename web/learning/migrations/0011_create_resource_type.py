from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0010_alter_learningresource_table_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResourceType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "slug",
                    models.SlugField(blank=True, max_length=100, unique=True),
                ),
                (
                    "content_kind",
                    models.CharField(
                        choices=[
                            ("video", "Video / Audio"),
                            ("reading", "Reading"),
                        ],
                        default="video",
                        max_length=20,
                    ),
                ),
                (
                    "is_system",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "System types are pre-seeded "
                            "and cannot be deleted."
                        ),
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "resource_type",
                "ordering": ["-is_system", "name"],
            },
        ),
    ]
