from django.contrib import messages
from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class AppointmentListView(ListView):
    model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name = "appointments"


class AppointmentBookView(LoginRequiredMixin, View):

    def post(self, request, pk):
        appointment = get_object_or_404(
            Appointment,
            pk=pk,
            user__isnull=True
        )

        appointment.user = request.user
        appointment.save()

        messages.success(request, "Appointment booked successfully.")

        return redirect(
            "appointment_detail",
            pk=appointment.pk
        )


class AppointmentCancelView(LoginRequiredMixin, View):

    def post(self, request, pk):
        appointment = get_object_or_404(
            Appointment,
            pk=pk,
            user=request.user
        )

        appointment.user = None
        appointment.save()

        messages.success(request, "Appointment cancelled successfully.")

        return redirect(
            "appointment"
        )


class AppointmentDetail(DetailView):
    model = Appointment
    template_name = "appointments/appointment_book.html"
    context_object_name = "appointment"
