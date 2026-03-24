from django.db.models import Sum

from learning.models import LearningResource

from .utils import calculate_percentage


def get_resource_progress(resource: LearningResource) -> dict[str, int]:
    """
    Calculate progress statistics for a learning resource.
    """
    units = resource.units.all().order_by("order")

    total_units = units.count()
    completed_units = units.filter(status="completed").count()
    remaining_units = total_units - completed_units

    completion_percentage = calculate_percentage(completed_units, total_units)

    total_duration = units.aggregate(total=Sum("duration_minutes"))["total"] or 0

    completed_duration = (
        units.filter(status="completed").aggregate(total=Sum("duration_minutes"))[
            "total"
        ]
        or 0
    )

    remaining_duration = total_duration - completed_duration

    return {
        "units": units,
        "total_units": total_units,
        "completed_units": completed_units,
        "remaining_units": remaining_units,
        "completion_percentage": completion_percentage,
        "total_duration": total_duration,
        "completed_duration": completed_duration,
        "remaining_duration": remaining_duration,
    }
