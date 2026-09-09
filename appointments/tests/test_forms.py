from appointments.forms import TimeSlotForm
from django.test import TestCase
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Speciality
from django_jalali.db import models as jmodels
import jdatetime
from datetime import time

User = get_user_model()

class TimeSlotFormTest(TestCase):
    
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
            
    

    def test_valid_form(self):
        data = {
            "doctor": self.doctor,
            "date": "2024-06-15",
            "start_time": "10:00",
            "end_time": "11:00",
            "price": 100,
        }

        form = TimeSlotForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "doctor": self.doctor,
            "date": "2024-06-15",
            "start_time": "10:00",
            "end_time": "11:00",
            "price": -100,
        }

        form = TimeSlotForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_fields(self):
        data = {
            "doctor": self.doctor,
            "date": "2024-06-15",
            "start_time": "10:00",
            "end_time": "11:00",
        }

        form = TimeSlotForm(data=data)
        self.assertFalse(form.is_valid())

    def test_clean_method(self):
        data = {
            "doctor": self.doctor,
            "date": "2024-06-15",
            "start_time": "10:00",
            "end_time": "11:00",
            "price": 100,
        }

        form = TimeSlotForm(data=data)
        self.assertTrue(form.is_valid())
        cleaned_data = form.clean()
        self.assertEqual(cleaned_data["doctor"], self.doctor)
        self.assertEqual(cleaned_data["date"],jdatetime.date(2024, 6, 15))
        self.assertEqual(cleaned_data["start_time"], time(10, 0))
        self.assertEqual(cleaned_data["end_time"], time(11, 0))
        self.assertEqual(cleaned_data["price"], 100)
