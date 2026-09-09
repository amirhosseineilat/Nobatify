from django.test import TestCase
from appointments.models import TimeSlot, Appointment
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Speciality
from django_jalali.db import models as jmodels
from datetime import time
from django.core.exceptions import ValidationError
from django.urls import reverse

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

        cls.speciality = Speciality.objects.create(
            name="Cardiology"
        )

        cls.doctor = Doctor.objects.create(
            first_name='ali',
            last_name='balochi',
            email='alibalochi@gmail.com',
            birth_date=jmodels.datetime.date(1381, 11, 8),
            medical_license_number="123456",
            phone="66557712",
            address="Tehran, Iran",
            bio="he is a highly skilled doctor with years of experience in his field.",
        )

        cls.doctor.specialities.add(cls.speciality)

        cls.time_slot = TimeSlot.objects.create(
            doctor=cls.doctor,
            start_time=time(10, 0),
            end_time=time(11, 0),
            price=100.00,
            is_reserved=False,
        )

        cls.appointment = Appointment.objects.create(
            doctor=cls.doctor,
            time_slot=cls.time_slot,
            patient=cls.user,
            paid=100.00,
        )

    def test_time_slot_list_view(self):

        url = reverse("appointment") 
        response = self.client.get(url)
        time_slots = response.context['timeslots']

        self.assertEqual(response.status_code,200)
        self.assertIn('timeslots',response.context)
        self.assertEqual(time_slots.count(),1)
        self.assertTemplateUsed(response,'appointments/timeslot_list.html')

    def test_my_appointment_list_view(self):

        url = reverse("my_appointment")
        response = self.client.get(url)
        timeslot = response.context['timeslot']

        self.assertEqual(response.status_code,200)
        self.assertIn('timeslot',response.context)
        self.assertEqual()
