from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import unauthenticated_user


@method_decorator(unauthenticated_user, name="dispatch")
class Login(View):
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("learning:dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return redirect("login")


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


@login_required
def settings(request):
    return render(request, "accounts/settings.html")
