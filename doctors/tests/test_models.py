from django.test import TestCase
from doctors.models import Doctor, Speciality, Comment
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels


User = get_user_model()

class DoctorModelTestCase(TestCase):
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
            
    def test_doctor_creation(self):
        self.assertEqual(self.doctor.first_name, "zizi")
        self.assertEqual(self.doctor.last_name, "soufi")
        self.assertEqual(self.doctor.email, "zizi.soufi@gmail.com")
        self.assertEqual(self.doctor.birth_date, jmodels.datetime.date(1360, 1, 1))
        self.assertEqual(self.doctor.medical_license_number, "123456")
        self.assertEqual(self.doctor.phone, "88776655")
        self.assertEqual(self.doctor.address, "123 Test Street")
        self.assertEqual(self.doctor.bio, "Test bio")
        # self.assertEqual(self.doctor.specialities, self.speciality)
        self.assertEqual(self.doctor.specialities.count(), 1)
        self.assertEqual(self.doctor.specialities.first(), self.speciality)
        
    def test_doctor_str_method(self):
        self.assertEqual(str(self.doctor), "zizi soufi")
        
    def test_doctor_speciality_relationship(self):
        self.assertIn(
            self.speciality,
            self.doctor.specialities.all()
        )

        self.assertIn(
            self.doctor,
            self.speciality.doctors.all()
        )
        
    def test_comment_creation(self):
        comment = Comment.objects.create(
            doctor=self.doctor,
            user=self.user,
            content="Great doctor!",
            rating=5
        )
        self.assertEqual(comment.doctor, self.doctor)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.content, "Great doctor!")
        self.assertEqual(comment.rating, 5)
        
    def test_comment_str_method(self):
        comment = Comment.objects.create(
            doctor=self.doctor,
            user=self.user,
            content="Great doctor!",
            rating=5
        )
        expected_str = f"Comment by {self.user.first_name} {self.user.last_name} on {self.doctor.first_name} {self.doctor.last_name}"
        self.assertEqual(str(comment), expected_str)
        
    def test_average_rating_and_comment_count(self):
        Comment.objects.create(doctor=self.doctor, user=self.user, content="Great doctor!", rating=5)
        Comment.objects.create(doctor=self.doctor, user=self.user, content="Good doctor!", rating=4)
        
        self.assertEqual(self.doctor.average_rating, 4.5)
        self.assertEqual(self.doctor.comment_count, 2)
    
    
    def test_doctor_average_rating_no_comments(self):
        self.assertEqual(self.doctor.average_rating, 0)
        self.assertEqual(self.doctor.comment_count, 0)
        
    def test_comment_rating_validation(self):
        
        with self.assertRaises(ValidationError):
            comment = Comment(
                    doctor=self.doctor,
                    user=self.user,
                    content="Invalid rating!",
                    rating=6
                )
            
            comment.full_clean()
            
            
        with self.assertRaises(ValidationError):
            comment = Comment(
                    doctor=self.doctor,
                    user=self.user,
                    content="Invalid rating!",
                    rating=0
                )
            
            comment.full_clean()
                