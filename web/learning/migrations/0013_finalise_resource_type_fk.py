import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Makes resource_type_new non-null, drops the legacy CharField,
    renames the FK to resource_type.

    Reverse uses explicit SQL to restore the legacy column as nullable
    VARCHAR so it does not hit a NOT NULL violation on existing rows.
    """

    dependencies = [
        ("learning", "0012_seed_and_add_resource_type_fk"),
    ]

    operations = [
        migrations.AlterField(
            model_name="learningresource",
            name="resource_type_new",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="resources",
                to="learning.resourcetype",
            ),
        ),
        migrations.RunSQL(
            sql=(
                "ALTER TABLE learning_resource "
                "DROP COLUMN resource_type_legacy"
            ),
            reverse_sql=(
                "ALTER TABLE learning_resource "
                "ADD COLUMN resource_type_legacy VARCHAR(50) DEFAULT 'other'"
            ),
            state_operations=[
                migrations.RemoveField(
                    model_name="learningresource",
                    name="resource_type_legacy",
                )
            ],
        ),
        migrations.RenameField(
            model_name="learningresource",
            old_name="resource_type_new",
            new_name="resource_type",
        ),
    ]
