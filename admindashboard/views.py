from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DeleteView,UpdateView,ListView
from doctors.models import Doctor,Speciality
from accounts.models import CustomUser
from appointments.models import TimeSlot,Appointment
from doctors.views import BaseCreateSpecialityView,BaseSearchDoctorView,BaseListDoctorView,BaseCreateDoctorView,BaseDetailDoctorView
from appointments.views import BaseTimeSlotListView,BaseTimeSlotCreateView
from django.urls import reverse_lazy
from django.contrib import messages
from doctors.forms import DoctorForm,SpecialityForm
from appointments.forms import TimeSlotForm
from django.db.models import Q
from django.contrib.auth.views import LoginView
from .forms import AdminLogingForm
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

#timeslots
class AdminListTimesLotView(BaseTimeSlotListView):
    template_name = "dashboard/admin_timeslot_list.html"
    def get_queryset(self):
        timeslots = TimeSlot.objects.all()
        return timeslots

class AdminCreateTimesLotView(BaseTimeSlotCreateView):
    template_name = "dashboard/admin_timeslot_create.html"
    success_url = reverse_lazy("admin_timeslots")

class AdminUpdaterTimeslotView(UpdateView):
    model = TimeSlot
    template_name = "dashboard/admin_timeslot_create.html"
    form_class = TimeSlotForm 
    success_url = reverse_lazy("admin_timeslots")

class AdminTimesLotDeleteView(DeleteView):
    model = TimeSlot
    success_url = reverse_lazy("admin_timeslots")
    

    def post(self,request,pk):
        try:
            timeslot = self.get_object()
            timeslot.delete()
            messages.success(request,"delete successfuly complited")
            return redirect("admin_timeslots")
        except Exception as e:
            messages.error(request,"delete failed")
            return redirect("admin_timeslots")

class AdminTimeSlotSearchView(ListView):
    template_name = "dashboard/admin_timeslot_list.html"
    context_object_name = "timeslots"

    def get_queryset(self):
        q = self.request.GET.get("q")
        if q:
            timeslots = TimeSlot.objects.filter(Q(doctor__first_name__icontains=q) | Q(doctor__email__icontains=q))

        return timeslots


    
class AdminLoginView(LoginView):

    template_name = 'dashboard/login.html'
    authentication_form = AdminLogingForm

    def get_success_url(self):
        return reverse_lazy("admin_dashboard")

#speciality
class AdminSpecialityListView(ListView):
    model = Speciality
    template_name = "dashboard/admin_speciality_list.html"
    context_object_name = "specialitys"


class AdminCreaterSpecialityView(BaseCreateSpecialityView):
    template_name = "dashboard/admin_speciality_create.html"
    success_url = reverse_lazy("admin_speciality_list")

class AdminUpdateSpecialityView(UpdateView):
    model = Speciality
    template_name = "dashboard/admin_speciality_create.html"
    form_class = SpecialityForm
    success_url = reverse_lazy("admin_speciality_list")

class AdminSpecialityDeleteView(DeleteView):
    model = Speciality
    success_url = reverse_lazy("admin_speciality_list")
    

    def post(self,request,pk):
        try:
            speciality = self.get_object()
            speciality.delete()
            messages.success(request,"حذف با موفقیت انجام شد")
            return redirect("admin_speciality_list")
        except Exception as e:
            messages.error(request,"حذف ناموفق بود")
            return redirect("admin_speciality_list")

class AdminSearchSpeciality(AdminSpecialityListView):
    def get_queryset(self):
        q = self.request.GET.get("q")
        if q:
            specialitys = Speciality.objects.filter(name__icontains=q)
        return specialitys