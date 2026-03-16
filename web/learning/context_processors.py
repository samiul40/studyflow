from .models import LearningResource, LearningUnit


def admin_dashboard_stats(request):
    if not request.path.startswith("/admin"):
        return {}

    total_resources = LearningResource.objects.count()
    total_units = LearningUnit.objects.count()
    completed_units = LearningUnit.objects.filter(status="completed").count()

    completion_rate = 0
    if total_units > 0:
        completion_rate = int((completed_units / total_units) * 100)

    # Course progress data
    resources = LearningResource.objects.prefetch_related("units").order_by(
        "-created_at"
    )[:5]

    resource_progress = []

    for resource in resources:
        total = resource.units.count()
        completed = resource.units.filter(status="completed").count()

        percent = 0
        if total > 0:
            percent = int((completed / total) * 100)

        resource_progress.append(
            {
                "title": resource.title,
                "percent": percent,
            }
        )

    return {
        "total_resources": total_resources,
        "total_units": total_units,
        "completed_units": completed_units,
        "completion_rate": completion_rate,
        "resource_progress": resource_progress,
    }
