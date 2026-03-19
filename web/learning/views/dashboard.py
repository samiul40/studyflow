from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from learning.services.dashboard import get_dashboard_stats


@login_required
def dashboard_view(request):
    resource_type = request.GET.get("type")
    stats = get_dashboard_stats(
        user=request.user,
        resource_type=resource_type,
    )

    return render(request, "dashboard/dashboard.html", stats)
