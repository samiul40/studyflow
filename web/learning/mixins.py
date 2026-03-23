from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect


class UserPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """
    Ensures user is authenticated and has required permissions.
    """

    raise_exception = False  # redirect instead of 403

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        return redirect("index")
