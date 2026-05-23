import datetime
from typing import List, Optional, TypedDict

from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate, TruncWeek
from django.utils import timezone

from learning.models import LearningResource, LearningUnit, ResourceType

from .utils import calculate_percentage


class ResourceProgress(TypedDict):
    id: int
    title: str
    percent: int


class WeeklySummary(TypedDict):
    units_completed: int
    learning_time_minutes: int
    resources_worked_on: int
    daily_completions: list  # [{label, count}] Mon–Sun, current week


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
    weekly_completions: list
    weekly_summary: WeeklySummary


def get_dashboard_stats(user=None, resource_type=None) -> DashboardStats:
    """Return dashboard statistics for learning resources."""

    resource_qs, unit_qs = _build_querysets(user, resource_type)

    total_resources = resource_qs.count()
    total_units = unit_qs.count()
    completed_units = unit_qs.filter(status="completed").count()
    incomplete_units = total_units - completed_units
    completion_rate = calculate_percentage(completed_units, total_units)

    resource_progress = _get_resource_progress(resource_qs)
    most_progress = max(resource_progress, key=lambda x: x["percent"], default=None)
    least_progress = min(resource_progress, key=lambda x: x["percent"], default=None)
    recent_resources = resource_qs.select_related("resource_type").order_by(
        "-created_at"
    )[:5]

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
        "resource_types_with_counts": _get_resource_types_with_counts(user),
        "weekly_completions": _get_weekly_completions(unit_qs),
        "weekly_summary": _get_weekly_summary(unit_qs),
    }


def _build_querysets(user, resource_type):
    """Apply user and resource type filters to the base querysets."""
    resource_qs = LearningResource.objects.all()
    unit_qs = LearningUnit.objects.all()

    if user is not None:
        resource_qs = resource_qs.filter(user=user)
        unit_qs = unit_qs.filter(resource__user=user)

    if resource_type:
        resource_qs = resource_qs.filter(resource_type__slug=resource_type)
        unit_qs = unit_qs.filter(resource__resource_type__slug=resource_type)

    return resource_qs, unit_qs


def _get_resource_progress(resource_qs) -> List[ResourceProgress]:
    """Return per-resource completion percentages, sorted highest first."""
    resources = resource_qs.annotate(
        total_units_count=Count("units"),
        completed_units_count=Count(
            "units",
            filter=Q(units__status="completed"),
        ),
    ).order_by("-created_at")[:5]

    progress = [
        {
            "id": r.id,
            "title": r.title,
            "percent": calculate_percentage(
                r.completed_units_count, r.total_units_count
            ),
        }
        for r in resources
    ]

    return sorted(progress, key=lambda x: x["percent"], reverse=True)


def _get_resource_types_with_counts(user) -> list:
    """Return resource types with their resource counts for the given user."""
    if user is None:
        return []

    types = ResourceType.objects.filter(resources__user=user).annotate(
        count=Count("resources")
    )
    return [{"type": rt, "count": rt.count} for rt in types]


def _get_weekly_completions(unit_qs) -> list:
    """
    Return a list of 8 dicts covering the last 8 weeks (oldest → newest),
    each with a human-readable label and the number of units completed that week.

    Uses updated_at on completed units as a proxy for completion date.
    """
    now = timezone.now()

    # Normalise to the start of the current week (Monday 00:00:00)
    current_week_start = (now - datetime.timedelta(days=now.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    eight_weeks_ago = current_week_start - datetime.timedelta(weeks=7)

    # Aggregate completed units by week
    raw = (
        unit_qs.filter(status="completed", updated_at__gte=eight_weeks_ago)
        .annotate(week=TruncWeek("updated_at"))
        .values("week")
        .annotate(count=Count("id"))
    )
    weekly_map = {entry["week"].date(): entry["count"] for entry in raw}

    # Build the full 8-week series, filling gaps with zero
    result = []
    for i in range(8):
        week_start = eight_weeks_ago + datetime.timedelta(weeks=i)
        result.append(
            {
                "label": week_start.strftime("%-d %b"),
                "count": weekly_map.get(week_start.date(), 0),
            }
        )

    return result


def _get_weekly_summary(unit_qs) -> WeeklySummary:
    """
    Return stats for the current Monday–Sunday week.

    Uses updated_at on completed units as a proxy for completion date.
    """
    now = timezone.now()
    week_start = (now - datetime.timedelta(days=now.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    week_end = week_start + datetime.timedelta(weeks=1)

    completed_this_week = unit_qs.filter(
        status="completed",
        updated_at__gte=week_start,
        updated_at__lt=week_end,
    )

    units_completed = completed_this_week.count()
    learning_time_minutes = (
        completed_this_week.aggregate(total=Sum("duration_minutes"))["total"] or 0
    )
    resources_worked_on = completed_this_week.values("resource_id").distinct().count()

    # Day-by-day completions for the current week (Mon–Sun)
    raw_daily = (
        completed_this_week.annotate(day=TruncDate("updated_at"))
        .values("day")
        .annotate(count=Count("id"))
    )
    daily_map = {entry["day"]: entry["count"] for entry in raw_daily}

    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily_completions = [
        {
            "label": day_labels[i],
            "count": daily_map.get((week_start + datetime.timedelta(days=i)).date(), 0),
        }
        for i in range(7)
    ]

    return {
        "units_completed": units_completed,
        "learning_time_minutes": learning_time_minutes,
        "resources_worked_on": resources_worked_on,
        "daily_completions": daily_completions,
    }
