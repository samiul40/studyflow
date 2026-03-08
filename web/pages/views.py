# Django
from django.shortcuts import render


# Create your views here.
# TEMP to check
def index(request):
    return render(request, "pages/index.html")
