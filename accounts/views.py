from django.shortcuts import render
from django.contrib.auth import login
from .models import Wallet
from django.contrib.auth.models import User
from .forms import (
    RegistrationForm,
    LoginForm,
    LoginForm,
    ForgetForm,
    ChangePasswordForm,
)
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .service import AccountService, Sender, EmailNotification

# Create your views here.


class LogingView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        login(form.user)
        return super().form_valid(form)


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ChangePasswordView(FormView):
    pass


class ForgetPasswordView(FormView):
    template_name = "accounts/forget_password.html"
    form_class = ForgetForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if email:
            sender = Sender(EmailNotification())
            AccountService.request_password_reset(email, sender)
        return super().form_valid(form)


class Profile(DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "user"


class Wallet(DetailView):
    model = Wallet
    template_name = "accounts/wallet.html"
    context_object_name = "wallet"
