from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView,CreateView
from .forms import TimeSlotForm
from doctors.models import Doctor
from .models import Appointment,TimeSlot
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#base view
class BaseTimeSlotListView(ListView):

    context_object_name = "timeslots"
    paginate_by = 10

    def get_queryset(self):
        doctor_id = self.request.GET.get("doctor")
        if doctor_id:
            queryset = TimeSlot.objects.filter(doctor_id=doctor_id)
            return queryset

        queryset = TimeSlot.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_id = self.request.GET.get("doctor")
        if doctor_id:
            context["selected_doctor"] = Doctor.objects.filter(pk=doctor_id).first()

        return context

class BaseTimeSlotDetailView(DetailView):
    model = TimeSlot
    context_object_name = "timeslot"
class BaseTimeSlotCreateView(CreateView):
    model = TimeSlot
    form_class = TimeSlotForm
#public view

class TimeSlotListView(BaseTimeSlotListView):
    template_name = "appointments/timeslot_list.html"


class MyAppointmentListView(ListView):
    template_name = "appointments/my_appointment_list.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user).select_related(
            "doctor"
        ).select_related("time_slot")


class AppointmentBookView(LoginRequiredMixin, View):

    def post(self, request, pk):
        timeslot = get_object_or_404(TimeSlot,pk=pk,is_reserved=False)

        appointment = Appointment(doctor=timeslot.doctor,time_slot=timeslot,patient=request.user)
        timeslot.is_reserved = True
        appointment.save()
        timeslot.save()

        messages.success(request, "Appointment booked successfully.")

        return redirect("my_appointment")


class AppointmentCancelView(LoginRequiredMixin, View):

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
        try:
            timeslot = appointment.time_slot
            appointment.delete()
            timeslot.is_reserved = False
            timeslot.save()
        except Exception as e :
            print(e)



        messages.success(request, "Appointment cancelled successfully.")

        return redirect("my_appointment")


class AppointmentDetail(DetailView):
    model = Appointment
    template_name = "appointments/appointment_book.html"
    context_object_name = "appointment"
