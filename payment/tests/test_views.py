from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Wallet
from payment.models import TransActoin


User = get_user_model()


class PaymentViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

        cls.wallet = Wallet.objects.create(
            user=cls.user,
            balance=Decimal("50000.00"),
        )

    def setUp(self):
        self.client.login(
            username="testuser",
            password="testpassword",
        )

    def test_send_payment_requires_login(self):
        """
        کاربر مهمان نباید بتواند payment ایجاد کند.
        """

        self.client.logout()

        response = self.client.post(
            reverse("send_info_payment"),
            {"balance": "100000"},
        )

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            "/accounts/login/",
            response.url,
        )

    @patch("payment.views.SandBoxPayment.send_information")
    @patch("payment.views.SandBoxPayment.redirect_to_zarinpal")
    def test_send_payment_success(
        self,
        mock_redirect,
        mock_send_information,
    ):
        """
        در صورت موفق بودن درخواست به زرین پال:

        1. transaction ساخته شود
        2. authority ذخیره شود
        3. کاربر به زرین پال redirect شود
        """

        authority = "A000000000000000000001"

        mock_send_information.return_value = (
            True,
            {
                "data": {
                    "authority": authority,
                }
            },
        )

        mock_redirect.return_value = (
            "https://sandbox.zarinpal.com/pg/StartPay/"
            + authority
        )

        response = self.client.post(
            reverse("send_info_payment"),
            {"balance": "100000"},
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.url,
            "https://sandbox.zarinpal.com/pg/StartPay/"
            + authority,
        )

        transaction = TransActoin.objects.get(
            authority=authority
        )

        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.amount, 100000)
        self.assertEqual(
            transaction.porpuse,
            "Charge Wallet",
        )

        mock_send_information.assert_called_once()
        mock_redirect.assert_called_once()

    @patch("payment.views.SandBoxPayment.send_information")
    def test_send_payment_gateway_failure(
        self,
        mock_send_information,
    ):
        """
        اگر زرین پال درخواست را قبول نکند،
        نباید transaction ساخته شود.
        """

        mock_send_information.return_value = (
            False,
            None,
        )

        response = self.client.post(
            reverse("send_info_payment"),
            {"balance": "100000"},
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.url,
            reverse("wallet"),
        )

        self.assertEqual(
            TransActoin.objects.count(),
            0,
        )

    @patch("payment.views.SandBoxPayment.send_information")
    def test_send_payment_without_authority(
        self,
        mock_send_information,
    ):
        """
        اگر response زرین پال authority نداشته باشد،
        View باید خطا را مدیریت کند.
        """

        mock_send_information.return_value = (
            True,
            {
                "data": {}
            },
        )

        response = self.client.post(
            reverse("send_info_payment"),
            {"balance": "100000"},
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.url,
            reverse("wallet"),
        )

        self.assertEqual(
            TransActoin.objects.count(),
            0,
        )

    def test_verify_payment_requires_login(self):
        """
        Verify نیز فقط برای کاربر لاگین شده است.
        """

        self.client.logout()

        response = self.client.get(
            reverse("verify_payment"),
            {
                "Authority": "A123456",
                "Status": "OK",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            "/accounts/login/",
            response.url,
        )

    def test_verify_payment_status_not_ok(self):
        """
        اگر Status زرین پال OK نباشد،
        نباید verify انجام شود.
        """

        response = self.client.get(
            reverse("verify_payment"),
            {
                "Authority": "A123456",
                "Status": "NOK",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.url,
            reverse("wallet"),
        )

        self.wallet.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("50000.00"),
        )

    @patch("payment.views.SandBoxPayment.verify")
    def test_verify_payment_success_code_100(
        self,
        mock_verify,
    ):
        """
        code=100 یعنی پرداخت موفق.

        باید:
        - card_number ذخیره شود
        - fee ذخیره شود
        - موجودی wallet افزایش پیدا کند
        """

        transaction = TransActoin.objects.create(
            user=self.user,
            porpuse="Charge Wallet",
            amount=100000,
            authority="A123456",
        )

        mock_verify.return_value = (
            True,
            {
                "data": {
                    "code": 100,
                    "card_pan": "603799******1234",
                    "fee": 1000,
                }
            },
        )

        response = self.client.get(
            reverse("verify_payment"),
            {
                "Authority": transaction.authority,
                "Status": "OK",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.url,
            reverse("wallet"),
        )

        transaction.refresh_from_db()
        self.wallet.refresh_from_db()

        self.assertEqual(
            transaction.card_number,
            "603799******1234",
        )

        self.assertEqual(
            transaction.fee,
            1000,
        )

        self.assertEqual(
            self.wallet.balance,
            Decimal("150000.00"),
        )

    @patch("payment.views.SandBoxPayment.verify")
    def test_verify_payment_success_code_101(
        self,
        mock_verify,
    ):
        """
        code=101 نیز در کد فعلی پروژه success محسوب می‌شود.
        """

        transaction = TransActoin.objects.create(
            user=self.user,
            porpuse="Charge Wallet",
            amount=50000,
            authority="A101010",
        )

        mock_verify.return_value = (
            True,
            {
                "data": {
                    "code": 101,
                    "card_pan": "603799******9999",
                    "fee": 500,
                }
            },
        )

        response = self.client.get(
            reverse("verify_payment"),
            {
                "Authority": transaction.authority,
                "Status": "OK",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.wallet.refresh_from_db()
        transaction.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("100000.00"),
        )

        self.assertEqual(
            transaction.card_number,
            "603799******9999",
        )

        self.assertEqual(
            transaction.fee,
            500,
        )

    @patch("payment.views.SandBoxPayment.verify")
    def test_verify_payment_failed(
        self,
        mock_verify,
    ):
        """
        اگر verify از نظر HTTP موفق باشد ولی status code
        پرداخت 100/101 نباشد، موجودی نباید افزایش پیدا کند.
        """

        transaction = TransActoin.objects.create(
            user=self.user,
            porpuse="Charge Wallet",
            amount=100000,
            authority="AFAILED",
        )

        mock_verify.return_value = (
            True,
            {
                "data": {
                    "code": -1,
                    "card_pan": None,
                    "fee": 0,
                }
            },
        )

        response = self.client.get(
            reverse("verify_payment"),
            {
                "Authority": transaction.authority,
                "Status": "OK",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.wallet.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("50000.00"),
        )

    @patch("payment.views.SandBoxPayment.verify")
    def test_verify_gateway_failure(
        self,
        mock_verify,
    ):
        """
        اگر ارتباط با درگاه برای verify شکست بخورد،
        موجودی نباید تغییر کند.
        """

        transaction = TransActoin.objects.create(
            user=self.user,
            porpuse="Charge Wallet",
            amount=100000,
            authority="AGATEWAYFAIL",
        )

        mock_verify.return_value = (
            False,
            None,
        )

        response = self.client.get(
            reverse("verify_payment"),
            {
                "Authority": transaction.authority,
                "Status": "OK",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.url,
            reverse("wallet"),
        )

        self.wallet.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("50000.00"),
        )

