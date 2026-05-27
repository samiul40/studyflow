from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import ChangePasswordForm, ProfileUpdateForm


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
