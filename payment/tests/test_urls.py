from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from payment.views import SendPaymentInfoView, VerifyPaymentView

User = get_user_model()


class PaymentURLsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123!",
        )

    def test_send_info_payment_url_resolves(self):
        resolver = resolve("/payment/send_info_payment/")
        self.assertEqual(resolver.func.view_class, SendPaymentInfoView)
        self.assertEqual(resolver.url_name, "send_info_payment")

    def test_verify_payment_url_resolves(self):
        resolver = resolve("/payment/verify/")
        self.assertEqual(resolver.func.view_class, VerifyPaymentView)
        self.assertEqual(resolver.url_name, "verify_payment")

    def test_send_info_payment_reverse(self):
        url = reverse("send_info_payment")
        self.assertEqual(url, "/payment/send_info_payment/")

    def test_verify_payment_reverse(self):
        url = reverse("verify_payment")
        self.assertEqual(url, "/payment/verify/")

    def test_send_info_payment_requires_login(self):
        response = self.client.post(reverse("send_info_payment"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_verify_payment_requires_login(self):
        response = self.client.get(reverse("verify_payment"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_send_info_payment_allowed_when_logged_in(self):
        self.client.login(username="testuser", password="StrongPass123!")
        response = self.client.post(reverse("send_info_payment"), data={"balance": "10000"})
        self.assertNotEqual(response.status_code, 403)