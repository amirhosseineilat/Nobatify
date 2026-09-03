from django.shortcuts import render
from django.views.generic import ListView,DeleteView,UpdateView,DetailView
from django.contrib.auth.views import LoginView
from .forms import AdminLogingForm
from django.urls import reverse_lazy

# Create your views here.

class AdminLoginView(LoginView):

	template_name = 'accounts/dashboard/login.html'
	authentication_form = AdminLogingForm
	success_url = reverse_lazy('admin_dashboard')