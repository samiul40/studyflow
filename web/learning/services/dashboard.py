from django.db.models import Count, Q

from learning.models import LearningResource, LearningUnit


def calculate_percentage(part, total):
    return int((part / total) * 100) if total > 0 else 0


def get_dashboard_stats():
    """
    Return aggregated dashboard statistics.
    Used for admin dashboard and future frontend dashboard.
    """

    total_resources = LearningResource.objects.count()
    total_units = LearningUnit.objects.count()
    completed_units = LearningUnit.objects.filter(status="completed").count()

    incomplete_units = total_units - completed_units
    completion_rate = calculate_percentage(completed_units, total_units)

    resources = LearningResource.objects.annotate(
        total_units_count=Count("units"),
        completed_units_count=Count(
            "units",
            filter=Q(units__status="completed"),
        ),
    ).order_by("-created_at")[:5]

    resource_progress = []

    for resource in resources:
        percent = calculate_percentage(
            resource.completed_units_count,
            resource.total_units_count,
        )

        resource_progress.append(
            {
                "id": resource.id,
                "title": resource.title,
                "percent": percent,
                "total_units": resource.total_units_count,
                "completed_units": resource.completed_units_count,
            }
        )

    most_progress = max(resource_progress, key=lambda x: x["percent"], default=None)
    least_progress = min(resource_progress, key=lambda x: x["percent"], default=None)

    recent_resources = LearningResource.objects.order_by("-created_at")[:5]

    return {
        "total_resources": total_resources,
        "total_units": total_units,
        "completed_units": completed_units,
        "incomplete_units": incomplete_units,
        "completion_rate": completion_rate,
        "resource_progress": resource_progress,
        "most_progress": most_progress,
        "least_progress": least_progress,
        "recent_resources": recent_resources,
    }
