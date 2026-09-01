from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth import login
from .models import Wallet
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    RegistrationForm,
    LoginForm,
    ForgetForm,
    ValidateOTPForm,
)
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .service import AccountService
from datetime import timedelta
from utils.notifications import Sender, EmailNotification

# Create your views here.


class LogingView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

class LogoutView(LogoutView):
    next_page = reverse_lazy("login")

class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ChangePasswordView(FormView):
    template_name = "accounts/change_password.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("reset_verified"):
            return redirect("forget_password")
        if not request.session.get("reset_user_id"):
            return redirect("forget_password")
        if now().timestamp() > request.session.get("rest_expire_time"):
            request.session.pop("reset_verified", None)
            request.session.pop("reset_user_id", None)
            request.session.pop("rest_expire_time", None)
            return redirect("forget_password")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.session.get("reset_user_id")
        if user_id:
            user = User.objects.get(id=user_id)
            kwargs["user"] = user
        return kwargs

    def form_valid(self, form):
        form.save()
        self.request.session.pop("reset_verified", None)
        self.request.session.pop("reset_user_id", None)
        self.request.session.pop("rest_expire_time", None)
        return super().form_valid(form)


class ForgetPasswordView(FormView):
    template_name = "accounts/forget_password.html"
    form_class = ForgetForm
    success_url = reverse_lazy("validate_otp")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        print("email", email)
        if email:
            sender = Sender(EmailNotification())
            AccountService.request_password_reset(email, sender)
        return super().form_valid(form)


class ValidateOtpView(FormView):

    template_name = "accounts/validate_otp.html"
    form_class = ValidateOTPForm
    success_url = reverse_lazy("change_password")

    def form_valid(self, form):
        status, user = AccountService.validate_otp(
            form.cleaned_data["otp_code"], "password_reset"
        )
        if status:
            self.request.session["reset_user_id"] = user.id
            self.request.session["reset_verified"] = True
            self.request.session["rest_expire_time"] = (
                now() + timedelta(minutes=2)
            ).timestamp()
            return super().form_valid(form)
        print("validate otp failed")
        return redirect("forget_password")


class Profile(LoginRequiredMixin, DetailView):
    template_name = "accounts/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user


class Wallet(LoginRequiredMixin, DetailView):
    template_name = "accounts/wallet.html"
    context_object_name = "wallet"

    def get_object(self):
        return self.request.user


class Home(TemplateView):
    template_name = "home.html"
