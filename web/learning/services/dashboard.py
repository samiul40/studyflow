from django.db.models import Count, Q

from learning.models import LearningResource, LearningUnit


def calculate_percentage(part, total):
    return int((part / total) * 100) if total > 0 else 0


def get_dashboard_stats(user=None, resource_type=None) -> dict:
    """
    Return dashboard statistics for learning resources.

    Supports filtering by user and resource type. Used for both
    admin and user dashboards.
    """

    resource_qs = LearningResource.objects.all()
    unit_qs = LearningUnit.objects.all()

    if user is not None:
        resource_qs = resource_qs.filter(user=user)
        unit_qs = unit_qs.filter(resource__user=user)

    if resource_type:
        resource_qs = resource_qs.filter(resource_type=resource_type)
        unit_qs = unit_qs.filter(resource__resource_type=resource_type)

    total_resources = resource_qs.count()
    total_units = unit_qs.count()
    completed_units = unit_qs.filter(status="completed").count()

    incomplete_units = total_units - completed_units
    completion_rate = calculate_percentage(completed_units, total_units)

    resources = resource_qs.annotate(
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
            }
        )

    resource_progress = sorted(
        resource_progress,
        key=lambda x: x["percent"],
        reverse=True,
    )

    most_progress = max(resource_progress, key=lambda x: x["percent"], default=None)
    least_progress = min(resource_progress, key=lambda x: x["percent"], default=None)

    recent_resources = resource_qs.order_by("-created_at")[:5]

    type_counts_raw = (
        LearningResource.objects.filter(user=user)
        .values("resource_type")
        .annotate(count=Count("id"))
    )

    type_counts_map = {item["resource_type"]: item["count"] for item in type_counts_raw}

    type_counts = {
        "youtube": type_counts_map.get("youtube", 0),
        "udemy": type_counts_map.get("udemy", 0),
        "book": type_counts_map.get("book", 0),
        "other": type_counts_map.get("other", 0),
    }

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
        "active_filter": resource_type,
        "type_counts": type_counts,
    }
