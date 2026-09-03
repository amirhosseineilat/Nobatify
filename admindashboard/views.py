from django.shortcuts import render
from django.views.generic import ListView,DeleteView,UpdateView,DetailView
from django.contrib.auth.views import LoginView
from .forms import AdminLoginForm
from django.urls import reverse_lazy

# Create your views here.

class AdminLoginView(LoginView):

	template_name = 'socialaccount/login.html'
	authentication_form = AdminLoginForm
	success_url = reverse_lazy('admin_dashboard')