# Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
# TEMP to check


@login_required
def index(request):
    return render(request, "pages/index.html")
