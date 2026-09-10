from datetime import timedelta
from unittest.mock import Mock, patch

from django.test import TestCase
from django.utils.timezone import now

from accounts.models import CustomUser, Otp
from accounts.service import AccountService


class AccountServiceTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="amir",
            email="amir@example.com",
            password="12345678",
        )

        self.sender = Mock()

    @patch("accounts.services.messages")
    def test_request_password_reset_success(self, mock_messages):

        result = AccountService.request_password_reset(
            request=Mock(),
            user_email="amir@example.com",
            sender=self.sender,
        )

        self.assertTrue(result)

        otp = Otp.objects.get(user=self.user)

        self.assertEqual(
            otp.purpose,
            "password_reset",
        )

        self.assertEqual(
            len(otp.code),
            6,
        )

        self.assertTrue(otp.code.isdigit())

        self.sender.send_notification.assert_called_once()

        mock_messages.success.assert_called_once()

    @patch("accounts.services.messages")
    def test_request_password_reset_user_not_found(
        self,
        mock_messages,
    ):

        result = AccountService.request_password_reset(
            request=Mock(),
            user_email="notfound@example.com",
            sender=self.sender,
        )

        self.assertFalse(result)

        self.assertEqual(
            Otp.objects.count(),
            0,
        )

        self.sender.send_notification.assert_not_called()

        mock_messages.error.assert_called_once()

    @patch("accounts.services.messages")
    def test_request_password_reset_sender_error(
        self,
        mock_messages,
    ):

        self.sender.send_notification.side_effect = Exception("Email service failed")

        result = AccountService.request_password_reset(
            request=Mock(),
            user_email="amir@example.com",
            sender=self.sender,
        )

        self.assertFalse(result)

        mock_messages.error.assert_called_once()

    @patch("accounts.services.messages")
    def test_validate_otp_success(self, mock_messages):

        otp = Otp.objects.create(
            user=self.user,
            code="123456",
            expire_time=now() + timedelta(minutes=2),
            purpose="password_reset",
            is_used=False,
        )

        result, user = AccountService.validate_otp(
            request=Mock(),
            otp_code="123456",
            purpose="password_reset",
        )

        self.assertTrue(result)

        self.assertEqual(
            user,
            self.user,
        )

        otp.refresh_from_db()

        self.assertTrue(otp.is_used)

        mock_messages.error.assert_not_called()

    @patch("accounts.services.messages")
    def test_validate_otp_invalid_code(
        self,
        mock_messages,
    ):

        Otp.objects.create(
            user=self.user,
            code="123456",
            expire_time=now() + timedelta(minutes=2),
            purpose="password_reset",
            is_used=False,
        )

        result, user = AccountService.validate_otp(
            request=Mock(),
            otp_code="999999",
            purpose="password_reset",
        )

        self.assertFalse(result)

        self.assertIsNone(user)

        mock_messages.error.assert_called_once()

    @patch("accounts.services.messages")
    def test_validate_otp_expired(
        self,
        mock_messages,
    ):

        otp = Otp.objects.create(
            user=self.user,
            code="123456",
            expire_time=now() - timedelta(minutes=1),
            purpose="password_reset",
            is_used=False,
        )

        result, user = AccountService.validate_otp(
            request=Mock(),
            otp_code="123456",
            purpose="password_reset",
        )

        self.assertFalse(result)

        self.assertIsNone(user)

        # OTP نباید used شود
        otp.refresh_from_db()

        self.assertFalse(otp.is_used)

        mock_messages.error.assert_called_once()

    @patch("accounts.services.messages")
    def test_validate_otp_already_used(
        self,
        mock_messages,
    ):

        otp = Otp.objects.create(
            user=self.user,
            code="123456",
            expire_time=now() + timedelta(minutes=2),
            purpose="password_reset",
            is_used=True,
        )

        result, user = AccountService.validate_otp(
            request=Mock(),
            otp_code="123456",
            purpose="password_reset",
        )

        self.assertFalse(result)

        self.assertIsNone(user)

        mock_messages.error.assert_called_once()

    @patch("accounts.services.messages")
    def test_validate_otp_wrong_purpose(
        self,
        mock_messages,
    ):

        Otp.objects.create(
            user=self.user,
            code="123456",
            expire_time=now() + timedelta(minutes=2),
            purpose="password_reset",
            is_used=False,
        )

        result, user = AccountService.validate_otp(
            request=Mock(),
            otp_code="123456",
            purpose="login",
        )

        self.assertFalse(result)

        self.assertIsNone(user)

        mock_messages.error.assert_called_once()
