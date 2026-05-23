from typing import List, Optional, TypedDict

from django.db.models import Count, Q

from learning.models import LearningResource, LearningUnit, ResourceType

from .utils import calculate_percentage


class ResourceProgress(TypedDict):
    id: int
    title: str
    percent: int


class DashboardStats(TypedDict):
    total_resources: int
    total_units: int
    completed_units: int
    incomplete_units: int
    completion_rate: int
    resource_progress: List[ResourceProgress]
    most_progress: Optional[ResourceProgress]
    least_progress: Optional[ResourceProgress]
    recent_resources: list
    active_filter: Optional[str]
    resource_types_with_counts: list


def get_dashboard_stats(user=None, resource_type=None) -> DashboardStats:
    """
    Return dashboard statistics for learning resources.

    Supports filtering by user and resource type slug.
    """

    resource_qs = LearningResource.objects.all()
    unit_qs = LearningUnit.objects.all()

    if user is not None:
        resource_qs = resource_qs.filter(user=user)
        unit_qs = unit_qs.filter(resource__user=user)

    if resource_type:
        resource_qs = resource_qs.filter(resource_type__slug=resource_type)
        unit_qs = unit_qs.filter(resource__resource_type__slug=resource_type)

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
            {"id": resource.id, "title": resource.title, "percent": percent}
        )

    resource_progress = sorted(
        resource_progress, key=lambda x: x["percent"], reverse=True
    )

    most_progress = max(resource_progress, key=lambda x: x["percent"], default=None)
    least_progress = min(resource_progress, key=lambda x: x["percent"], default=None)

    recent_resources = resource_qs.select_related("resource_type").order_by(
        "-created_at"
    )[:5]

    if user is not None:
        types_for_user = ResourceType.objects.filter(resources__user=user).annotate(
            count=Count("resources")
        )
        resource_types_with_counts = [
            {"type": rt, "count": rt.count} for rt in types_for_user
        ]
    else:
        resource_types_with_counts = []

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
        "resource_types_with_counts": resource_types_with_counts,
    }
