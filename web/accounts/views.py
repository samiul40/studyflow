from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import unauthenticated_user
from .forms import ChangePasswordForm, ProfileUpdateForm


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


class Settings(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            "accounts/settings.html",
            {
                "profile_form": ProfileUpdateForm(instance=request.user),
                "password_form": ChangePasswordForm(request.user),
            },
        )

    def post(self, request):
        form_type = request.POST.get("form_type")

        if form_type == "profile":
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            password_form = ChangePasswordForm(request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("settings")

        elif form_type == "password":
            profile_form = ProfileUpdateForm(instance=request.user)
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Password changed successfully.")
                return redirect("settings")

        else:
            return redirect("settings")

        return render(
            request,
            "accounts/settings.html",
            {
                "profile_form": profile_form,
                "password_form": password_form,
            },
        )
