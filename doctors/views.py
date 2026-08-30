from django.shortcuts import render
from .models import Doctor
from django.views.generic import (
    DetailView,
    ListView,
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