from datetime import time
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from doctors.models import Doctor, Speciality
from appointments.models import TimeSlot

User = get_user_model()


class AdminViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="Admin123456!",
            is_admin=True,
        )

        self.normal_user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="User123456!",
            is_admin=False,
        )

        self.client.force_login(self.admin)

        self.speciality = Speciality.objects.create(name="دندانپزشکی")

        self.doctor = Doctor.objects.create(
            first_name="محمد",
            last_name="احمدی",
            email="mohammad.ahmadi@example.com",
            birth_date="1365-08-15",
            medical_license_number="MED-784521",
            phone="91234567",
            address="تهران، خیابان ولیعصر",
            bio="پزشک متخصص با سابقه کاری بالا",
        )

        self.doctor.specialities.add(self.speciality)

        self.timeslot = TimeSlot.objects.create(
            doctor=self.doctor,
            date="1405-06-20",
            start_time=time(9, 0),
            end_time=time(9, 30),
            price=Decimal("500000.00"),
            is_reserved=False,
        )

    def test_admin_dashboard(self):
        response = self.client.get(reverse("admin_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["doctors_count"], 1)
        self.assertEqual(response.context["slots_count"], 1)
        self.assertEqual(response.context["appointments_count"], 0)
        self.assertEqual(response.context["users_count"], 2)

    def test_doctor_list(self):
        response = self.client.get(reverse("admin_doctor_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "محمد")
        self.assertContains(response, "احمدی")

    def test_doctor_detail(self):
        response = self.client.get(
            reverse("admin_doctor_detail", kwargs={"pk": self.doctor.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "محمد")
        self.assertContains(response, "احمدی")

    def test_doctor_create_page(self):
        response = self.client.get(reverse("admin_doctor_create"))

        self.assertEqual(response.status_code, 200)

    def test_doctor_update_page(self):
        response = self.client.get(
            reverse("admin_doctor_update", kwargs={"pk": self.doctor.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_doctor_delete(self):
        doctor_id = self.doctor.pk

        response = self.client.post(
            reverse("admin_doctor_delete", kwargs={"pk": doctor_id})
        )

        self.assertRedirects(response, reverse("admin_doctor_list"))

        self.assertFalse(Doctor.objects.filter(pk=doctor_id).exists())

    def test_doctor_search(self):
        response = self.client.get(reverse("admin_doctor_search"), {"q": "محمد"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "محمد")
        self.assertContains(response, "احمدی")

    def test_doctor_search_by_speciality(self):
        response = self.client.get(reverse("admin_doctor_search"), {"q": "دندانپزشکی"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "محمد")
        self.assertContains(response, "احمدی")

    def test_timeslot_list(self):
        response = self.client.get(reverse("admin_timeslots"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "09:00")

    def test_timeslot_create_page(self):
        response = self.client.get(reverse("admin_timeslot_create"))

        self.assertEqual(response.status_code, 200)

    def test_timeslot_update_page(self):
        response = self.client.get(
            reverse("admin_timeslot_update", kwargs={"pk": self.timeslot.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_timeslot_delete(self):
        timeslot_id = self.timeslot.pk

        response = self.client.post(
            reverse("admin_timeslot_delete", kwargs={"pk": timeslot_id})
        )

        self.assertRedirects(response, reverse("admin_timeslots"))

        self.assertFalse(TimeSlot.objects.filter(pk=timeslot_id).exists())

    def test_timeslot_search_by_doctor_name(self):
        response = self.client.get(reverse("admin_timeslot_search"), {"q": "محمد"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "09:00")

    def test_timeslot_search_by_email(self):
        response = self.client.get(
            reverse("admin_timeslot_search"), {"q": "mohammad.ahmadi@example.com"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "09:00")

    def test_speciality_list(self):
        response = self.client.get(reverse("admin_speciality_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "دندانپزشکی")

    def test_speciality_create_page(self):
        response = self.client.get(reverse("admin_speciality_create"))

        self.assertEqual(response.status_code, 200)

    def test_speciality_update_page(self):
        response = self.client.get(
            reverse("admin_speciality_update", kwargs={"pk": self.speciality.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_speciality_delete(self):
        speciality_id = self.speciality.pk

        response = self.client.post(
            reverse("admin_speciality_delete", kwargs={"pk": speciality_id})
        )

        self.assertRedirects(response, reverse("admin_speciality_list"))

        self.assertFalse(Speciality.objects.filter(pk=speciality_id).exists())

    def test_speciality_search(self):
        response = self.client.get(reverse("admin_speciality_search"), {"q": "دندان"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "دندانپزشکی")

    def test_admin_can_access_dashboard(self):
        response = self.client.get(reverse("admin_dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_anonymous_cannot_access_dashboard(self):
        self.client.logout()

        response = self.client.get(reverse("admin_dashboard"))

        self.assertRedirects(response, reverse("login"))

    def test_normal_user_cannot_access_dashboard(self):
        self.client.logout()
        self.client.force_login(self.normal_user)

        response = self.client.get(reverse("admin_dashboard"))

        self.assertRedirects(response, reverse("home"))
