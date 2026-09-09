

from django.test.testcases import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.forms import User


class PaymentViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password="testpassword",
        )    

    def test_payment_view_requires_login(self):
        url = reverse("payment")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/payment/")

    def test_payment_view_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("payment")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payment/payment.html")       