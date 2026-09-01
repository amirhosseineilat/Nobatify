from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Doctor
from django.views.generic import DetailView, ListView, CreateView
from .service import DoctorService

# Create your views here.


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "doctors/doctor_detail.html"
    context_object_name = "doctor"


class DoctorListView(ListView):
    model = Doctor
    template_name = "doctors/doctor_list.html"
    context_object_name = "doctors"


class CommentCreateView(LoginRequiredMixin, CreateView):
    pass


class SearchDoctorView(ListView):
    template_name = "doctors/doctor_list.html"
    context_object_name = "doctors"

    def get_queryset(self):
        q = self.request.GET.get("q")
        doctors = DoctorService.search(q)
        return doctors
