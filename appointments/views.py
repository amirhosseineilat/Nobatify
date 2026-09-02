from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from doctors.models import Doctor
from .models import Appointment,TimeSlot
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class AppointmentListView(ListView):
    # model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name = "appointments"

    def get_queryset(self):
        doctor_id = self.request.GET.get("doctor")
        if doctor_id:
            queryset = TimeSlot.objects.filter(doctor__id=doctor_id)
            return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_id = self.request.GET.get("doctor")
        if doctor_id:
            context["selected_doctor"] = Doctor.objects.filter(pk=doctor_id).first()

        return context


class MyAppointmentListView(ListView):
    model = Appointment
    template_name = "appointments/my_appointment_list.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user).select_related(
            "doctor"
        )


class AppointmentBookView(LoginRequiredMixin, View):

    def post(self, request, pk):
        timeslot = get_object_or_404(TimeSlot,pk=pk,is_reserved=False)

        appointment = Appointment(doctor=timeslot.doctor,time_slot=timeslot,patient=request.user)
        timeslot.is_reserved = True
        appointment.save()

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
            print("e")



        messages.success(request, "Appointment cancelled successfully.")

        return redirect("appointment")


class AppointmentDetail(DetailView):
    model = Appointment
    template_name = "appointments/appointment_book.html"
    context_object_name = "appointment"
