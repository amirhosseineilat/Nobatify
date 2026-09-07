from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from doctors.models import Doctor, Speciality, Comment
from appointments.models import TimeSlot, Appointment
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from doctors.forms import CommentForm
from datetime import time, timedelta
import datetime


User = get_user_model()

class DoctorDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
            cls.user = User.objects.create_user(
                username="testuser",
                first_name="Test",
                last_name="User",
                email="testuser@example.com",
                password="testpassword"
            )
            
            
            cls.speciality = Speciality.objects.create(name="atfal")
            
            
            cls.doctor = Doctor.objects.create(
                first_name="zizi",
                last_name="soufi",
                email="zizi.soufi@gmail.com",
                birth_date=jmodels.datetime.date(1360, 1, 1),
                medical_license_number="123456",
                phone="88776655",
                address="123 Test Street",
                bio="Test bio",
            )
            cls.doctor.specialities.add(cls.speciality)
            
            tomorrow = timezone.localdate() + timedelta(days=1)
        
        
            cls.available_slot_1 = TimeSlot.objects.create(
                doctor=cls.doctor,
                date=tomorrow, start_time=time(9, 0),
                end_time=time(10, 0),
                is_reserved=False
            )
            
            
            cls.available_slot_2 = TimeSlot.objects.create(
                doctor=cls.doctor,
                date=tomorrow, 
                start_time=time(10, 0),
                end_time=time(11, 0),
                is_reserved=False
            )
            
            
            cls.booked_slot = TimeSlot.objects.create(
                doctor=cls.doctor,
                date=tomorrow,
                start_time=time(11, 0),
                end_time=time(12, 0),
                is_reserved=False
            )
            
            
            cls.appointment = Appointment.objects.create(
                doctor=cls.doctor,
                patient=cls.user,
                time_slot=cls.booked_slot,
                
            )
            
            cls.url = reverse("doctor_detail", kwargs={"pk": cls.doctor.pk})
            
    def test_doctor_detail_view_success(self):
        
        url = reverse("doctor_detail", kwargs={"pk": self.doctor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["doctor"], self.doctor)
        
        
    def test_doctor_detail_view_error(self):
        
        invalid_url = reverse("doctor_detail", kwargs={"pk": self.doctor.pk + 1000})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)
        
        
    def test_detail_view_uses_correct_template(self):
        url = reverse("doctor_detail", kwargs={"pk": self.doctor.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "doctors/doctor_detail.html")
        
        
    def test_available_time_slots(self):
        
        url = reverse("doctor_detail", kwargs={"pk": self.doctor.pk})
        response = self.client.get(url)
        doctor = response.context["doctor"]
       
        self.assertTrue(hasattr(doctor, "available_time_slots"))
        
        expected_slots = TimeSlot.objects.filter(
            doctor=self.doctor,
            appointment__isnull=True
        )
        
        self.assertEqual(
            list(doctor.available_time_slots),
            list(expected_slots)
        )
        
        self.assertEqual(len(doctor.available_time_slots), 2)
        
        self.assertIn(self.available_slot_1, doctor.available_time_slots)
        self.assertIn(self.available_slot_2, doctor.available_time_slots)
        self.assertNotIn(self.booked_slot, doctor.available_time_slots)
        
    def test_detail_view_contains_doctor_info(self):
        url = reverse("doctor_detail", kwargs={"pk": self.doctor.pk})
        response = self.client.get(url)
        
        doctor_from_db = Doctor.objects.get(pk=self.doctor.pk)
        expected_date = str(doctor_from_db.birth_date)

        self.assertContains(response, self.doctor.first_name)
        self.assertContains(response, self.doctor.last_name)
        self.assertContains(response, self.doctor.email)
        self.assertContains(response, expected_date)
        self.assertContains(response, self.doctor.medical_license_number)
        self.assertContains(response, self.doctor.phone)
        self.assertContains(response, self.doctor.address)
        self.assertContains(response, self.doctor.bio)
        
        
    def test_detail_view_context_has_comment_form(self):
        url = reverse("doctor_detail", kwargs={"pk": self.doctor.pk})
        response = self.client.get(url)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], CommentForm)
        
        
    def test_average_rating_and_total_comments(self):
        Comment.objects.create(doctor=self.doctor, user=self.user, content="Great doctor!", rating=5)
        Comment.objects.create(doctor=self.doctor, user=self.user, content="Good doctor!", rating=4)
        
        url = reverse("doctor_detail", kwargs={"pk": self.doctor.pk})
        response = self.client.get(url)
        doctor = response.context["doctor"]
        
        self.assertEqual(doctor.average_rating, 4.5)
        self.assertEqual(doctor.comment_count, 2)
        
        self.assertTrue(hasattr(doctor, "avg_rating"))
        self.assertTrue(hasattr(doctor, "total_comments"))
        
        
        self.assertEqual(float(doctor.avg_rating), 4.5)  
        self.assertEqual(doctor.total_comments, 2)

    
