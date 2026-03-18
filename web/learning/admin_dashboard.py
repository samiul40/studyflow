from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from learning.services.dashboard import get_dashboard_stats


@staff_member_required
def admin_dashboard(request):
    context = get_dashboard_stats()
    return render(request, "admin/index.html", context)
