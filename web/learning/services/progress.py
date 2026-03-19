from django.db.models import Sum


def get_resource_progress(resource):
    """
    Calculate progress statistics for a learning resource.
    """
    units = resource.units.all().order_by("order")

    total_units = units.count()
    completed_units = units.filter(status="completed").count()
    remaining_units = total_units - completed_units

    completion_percentage = (
        round((completed_units / total_units) * 100) if total_units > 0 else 0
    )

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
