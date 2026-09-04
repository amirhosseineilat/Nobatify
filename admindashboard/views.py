from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DeleteView,UpdateView
from doctors.models import Doctor
from accounts.models import CustomUser
from appointments.models import TimeSlot,Appointment
from doctors.views import BaseSearchDoctorView,BaseListDoctorView,BaseCreateDoctorView,BaseDetailDoctorView
from django.urls import reverse_lazy
from django.contrib import messages
from doctors.forms import DoctorForm
# Create your views here.

class AdminDoctorListView(BaseListDoctorView):
    template_name = "dashboard/admin_doctors.html"
class AdminDashboardView( TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors_count"] = Doctor.objects.count()
        context["slots_count"] = TimeSlot.objects.count()
        context["appointments_count"] = Appointment.objects.count()
        context["users_count"] = CustomUser.objects.filter(is_active=True).count()
        return context

class AdminCreateDoctorView(BaseCreateDoctorView):
    template_name = "dashboard/admin_doctor_create.html"
    success_url = reverse_lazy("admin_doctor_list")
class AdminDoctorDetailView(BaseDetailDoctorView):
    pass
class AdminDoctorUpdateView(UpdateView):
    model = Doctor
    template_name = "dashboard/admin_doctor_create.html"
    form_class = DoctorForm
    success_url = reverse_lazy("admin_doctor_list")


class AdminDoctorDeleteView(DeleteView):
    model = Doctor
    success_url = reverse_lazy("admin_doctor_list")
    

    def post(self,request,pk):
        try:
            doctor = self.get_object()
            doctor.delete()
            messages.success(request,"delete successfuly complited")
            return redirect("admin_doctor_list")
        except Exception as e:
            messages.error(request,"delete failed")
            return redirect("admin_doctor_list")

class AdminSearchDoctor(BaseSearchDoctorView):
    template_name = "dashboard/admin_doctors.html"


