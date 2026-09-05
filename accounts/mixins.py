from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.is_admin
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("login")

        messages.error(
            self.request,
            "You do not have permission to access this page."
        )
        return redirect("home")
