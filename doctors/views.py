from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Doctor
from django.views.generic import (
    DetailView,
    ListView,
    CreateView
)
# Create your views here.

class DoctorDetailView(DetailView):
    model = Doctor
    tmplate_name = "doctors/doctor_detail.html"
    context_object_name = "doctor"
    
    
class DoctorListView(ListView):
    model = Doctor
    template_name = "doctors/doctor_list.html"
    context_object_name = "doctors"
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    pass