from django.test import TestCase
from appointments.models import TimeSlot, Appointment
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Speciality
from django_jalali.db import models as jmodels
from datetime import time
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from accounts.models import Wallet

User = get_user_model()


class AppointmentViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@gmail.com",
            password="testpassword",
        )

        cls.speciality = Speciality.objects.create(name="Cardiology")

        cls.doctor = Doctor.objects.create(
            first_name="ali",
            last_name="balochi",
            email="alibalochi@gmail.com",
            birth_date=jmodels.datetime.date(1381, 11, 8),
            medical_license_number="123456",
            phone="66557712",
            address="Tehran, Iran",
            bio="he is a highly skilled doctor with years of experience in his field.",
        )

        cls.doctor.specialities.add(cls.speciality)

        cls.wallet = Wallet.objects.create(
            user=cls.user,
            balance=1000,
        )

        tomorrow = timezone.localdate() + timedelta(days=1)

        cls.time_slot = TimeSlot.objects.create(
            doctor=cls.doctor,
            date=tomorrow,
            start_time=time(10, 0),
            end_time=time(11, 0),
            price=100.00,
            is_reserved=False,
        )


    def test_time_slot_list_view(self):

        url = reverse("appointment") + f"?doctor={self.doctor.pk}"
        response = self.client.get(url)
        time_slots = response.context["timeslots"]
        selected_doctor = response.context.get("selected_doctor")

        self.assertEqual(response.status_code, 200)
        self.assertIn("timeslots", response.context)
        self.assertEqual(time_slots.count(), 1)
        self.assertTemplateUsed(response, "appointments/timeslot_list.html")

    def test_my_appointment_list_view(self):

        self.client.login(username="testuser", password="testpassword")

        appointment = Appointment.objects.create(
        doctor=self.doctor,
        time_slot=self.time_slot,
        patient=self.user,
        paid=100.00,
    )
        url = reverse("my_appointment")
        response = self.client.get(url)
        appointments = response.context["appointments"]

        self.assertEqual(response.status_code, 200)
        self.assertIn("appointments", response.context)
        self.assertEqual(appointments.count(), 1)
        self.assertTemplateUsed(response, "appointments/my_appointment_list.html")
        self.assertEqual(appointments.first(), appointment)

    def test_book_appointment_view(self):
        self.client.login(username="testuser", password="testpassword")

        url = reverse("appointment_book", args=[self.time_slot.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.time_slot.refresh_from_db()
        self.assertTrue(self.time_slot.is_reserved)

    def test_cancel_appointment_view(self):
        self.client.login(
            username="testuser",
            password="testpassword"
        )

        appointment = Appointment.objects.create(
            doctor=self.doctor,
            time_slot=self.time_slot,
            patient=self.user,
            paid=100.00,
        )

        self.time_slot.is_reserved = True
        self.time_slot.save()

        url = reverse(
            "appointment_cancel",
            args=[appointment.pk]
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        self.time_slot.refresh_from_db()

        self.assertFalse(self.time_slot.is_reserved)

        self.assertFalse(
            Appointment.objects.filter(pk=appointment.pk).exists()
        )

    def test_appointment_detail_view(self):
        self.client.login(
            username="testuser",
            password="testpassword"
        )

        appointment = Appointment.objects.create(
            doctor=self.doctor,
            time_slot=self.time_slot,
            patient=self.user,
            paid=100.00,
        )

        url = reverse(
            "appointment_detail",
            args=[appointment.pk]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["appointment"],
            appointment
        )

        self.assertTemplateUsed(
            response,
            "appointments/appointment_book.html"
        )

    def test_appointment_detail_view_not_found(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("appointment_detail", args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_book_appointment_view_invalid_time_slot(self):
        self.client.login(username="testuser", password="testpassword")
        invalid_time_slot_id = 999
        url = reverse("appointment_book", args=[invalid_time_slot_id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
