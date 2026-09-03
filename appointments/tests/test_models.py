from django.test import TestCase
from appointments.models import TimeSlot,Appointment
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from django_jalali.db import models as jmodels

User = get_user_model()

class AppointmentModelTest(TestCase):

	@classmethod 
	def setUpTestdate(cls):
		cls.user = User.objects.create_user(
			username="testuser",
			first_name="Test",
			last_name="User",
			email="testuser@gmail.com",
			password="testpassword",
		)

		cls.doctor = Doctor(
			first_name = 'ali',
		    last_name = 'balochi',
		    email = 'alibalochi@gmail.com',
		    birth_date = jmodels.datetime.date(1381,11,8),
		    medical_license_number = "123456",
		    phone = models.CharField(max_length=8),
		    address = models.TextField(),
		    bio = models.TextField(),
		)

		cls.time_slot = TimeSlot(

		)