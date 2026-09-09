from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from admindashboard.forms import AdminLogingForm

User = get_user_model()


class AdminFormTestCase(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="Admin123456!",
            is_admin=True,
        )

        self.normal_user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="User123456!",
            is_admin=False,
        )

    def test_admin_user_can_login(self):
        form = AdminLogingForm(
            data={
                "username": "admin",
                "password": "Admin123456!",
            }
        )

        self.assertTrue(form.is_valid())

    def test_normal_user_cannot_login(self):
        form = AdminLogingForm(
            data={
                "username": "user",
                "password": "User123456!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "only admin user can login",
            form.errors["__all__"],
        )
