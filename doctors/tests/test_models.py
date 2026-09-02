from django.test import TestCase
from doctors.models import Doctor, Speciality, Comment
from django.contrib.auth.models import User


class DoctorModelTestCase(TestCase):
    def setUp(self):
            self.user = User.objects.create_user(
                username="testuser", 
                email="testuser@example.com",
                password="testpassword"
            )
            
            
            self.speciality = Speciality.objects.create(name="atfal")
            
            
            self.doctor = Doctor.objects.create(
                first_name="zizi",
                last_name="soufi",
                email="zizi.soufi@gmail.com",
                # specialities=self.speciality  
            )
            self.doctor.specialities.add(self.speciality)
            
    def test_doctor_creation(self):
        self.assertEqual(self.doctor.first_name, "zizi")
        self.assertEqual(self.doctor.last_name, "soufi")
        self.assertEqual(self.doctor.email, "zizi.soufi@gmail.com")
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
            self.speciality.doctor_set.all()
        )