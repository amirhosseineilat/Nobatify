from django.test import TestCase
from appointments.models import TimeSlot,Appointment
from django.contrib.auth import get_user_model
from doctors.models import Doctor,Speciality
from django_jalali.db import models as jmodels
from datetime import time
from django.core.exceptions import ValidationError

User = get_user_model()

class AppointmentModelTest(TestCase):

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
			name = "Cardiology"
		)

		cls.doctor = Doctor.objects.create(
			first_name = 'ali',
		    last_name = 'balochi',
		    email = 'alibalochi@gmail.com',
		    birth_date = jmodels.datetime.date(1381,11,8),
		    medical_license_number = "123456",
		    phone = "66557712",
		    address = "Tehran, Iran",
		    bio = "he is a highly skilled doctor with years of experience in his field.",
		)

		cls.doctor.specialities.add(cls.speciality)

		cls.time_slot = TimeSlot.objects.create(
			doctor = cls.doctor,
			start_time = time(10, 0),
			end_time = 	time(11, 0),
			price = 100.00,
			is_reserved = False,
		)

		cls.appointment = Appointment.objects.create(
			doctor = cls.doctor,
			time_slot = cls.time_slot,
			patient = cls.user,
			paid = 100.00,
		)

	def test_appointment_creation(self):
		self.assertEqual(self.appointment.doctor, self.doctor)
		self.assertEqual(self.appointment.time_slot, self.time_slot)
		self.assertEqual(self.appointment.patient, self.user)
		self.assertEqual(self.appointment.paid, 100.00)

	def test_appointment_str_method(self):
		expected_str = f"Appointment with {self.doctor} on {self.time_slot.date} at {self.time_slot.start_time}"
		self.assertEqual(str(self.appointment), expected_str)

	def test_time_slot_creation(self):
		self.assertEqual(self.time_slot.doctor, self.doctor)
		self.assertEqual(self.time_slot.start_time, time(10, 0))
		self.assertEqual(self.time_slot.end_time, time(11, 0))
		self.assertEqual(self.time_slot.price, 100.00)
		self.assertFalse(self.time_slot.is_reserved)

	def test_time_slot_str_method(self):
		expected_str = f"{self.doctor} - {self.time_slot.date} ({self.time_slot.start_time} - {self.time_slot.end_time}) | {self.time_slot.price}"
		self.assertEqual(str(self.time_slot), expected_str)		

	def test_time_slot_unique_constraint(self):
		with self.assertRaises(ValidationError):
			TimeSlot.objects.create(
				doctor = self.doctor,
				start_time = time(10, 0),
				end_time = time(11, 0),
				price = 150.00,
				is_reserved = False,
			)

	def test_appointment_paid_default(self):
		time_slot = TimeSlot.objects.create(
			doctor = self.doctor,
			start_time = time(11, 0),
			end_time = time(12, 0),
			price = 200.00,
			is_reserved = False,
		)

		appointment = Appointment.objects.create(
			doctor = self.doctor,
			time_slot = time_slot,
			patient = self.user,
		)

		self.assertEqual(appointment.paid, 200.00)

	def test_time_slot_price_validation(self):
		with self.assertRaises(ValidationError):
			time_slot = TimeSlot(
				doctor = self.doctor,
				start_time = time(12, 0),
				end_time = time(13, 0),
				price = -50.00,
				is_reserved = False,
			)
			time_slot.full_clean()

	def test_time_slot_end_time_after_start_time(self):
		with self.assertRaises(ValidationError):
			time_slot = TimeSlot(
				doctor = self.doctor,
				start_time = time(14, 0),
				end_time = time(13, 0),
				price = 100.00,
				is_reserved = False,
			)
			time_slot.full_clean()

