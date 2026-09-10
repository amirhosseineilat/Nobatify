from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.forms import (
    RegistrationForm,
    LoginForm,
    ForgetForm,
    ValidateOTPForm,
    CardForm,
)
from accounts.models import Wallet, Card

User = get_user_model()


class RegistrationFormTests(TestCase):
    def test_valid_form(self):
        data = {
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "email": "test@example.com",
            "first_name": "Ali",
            "last_name": "Rezaei",
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_password_mismatch(self):
        data = {
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "DifferentPass!",
            "email": "test@example.com",
            "first_name": "Ali",
            "last_name": "Rezaei",
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_missing_fields(self):
        form = RegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password1", form.errors)
        self.assertIn("password2", form.errors)
        self.assertIn("email", form.errors)

    def test_duplicate_username(self):
        User.objects.create_user(username="existing", email="a@example.com", password="Pass123!")
        data = {
            "username": "existing",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "email": "new@example.com",
            "first_name": "Ali",
            "last_name": "Rezaei",
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_duplicate_email(self):
        User.objects.create_user(username="user1", email="same@example.com", password="Pass123!")
        data = {
            "username": "user2",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "email": "same@example.com",
            "first_name": "Ali",
            "last_name": "Rezaei",
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_save_creates_user(self):
        data = {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "email": "newuser@example.com",
            "first_name": "Sara",
            "last_name": "Ahmadi",
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("StrongPass123!"))


class LoginFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="StrongPass123!",
        )

    def test_valid_login(self):
        form = LoginForm(data={"username": "loginuser", "password": "StrongPass123!"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_wrong_password(self):
        form = LoginForm(data={"username": "loginuser", "password": "WrongPass!"})
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_nonexistent_user(self):
        form = LoginForm(data={"username": "ghost", "password": "StrongPass123!"})
        self.assertFalse(form.is_valid())


class ForgetFormTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="forgetuser",
            email="forget@example.com",
            password="StrongPass123!",
        )

    def test_valid_email(self):
        form = ForgetForm(data={"email": "forget@example.com"})
        self.assertFalse(form.is_valid())

    def test_invalid_email_format(self):
        form = ForgetForm(data={"email": "not-an-email"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_empty_email(self):
        form = ForgetForm(data={"email": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class ValidateOTPFormTests(TestCase):
    def test_valid_otp(self):
        form = ValidateOTPForm(data={"otp_code": "123456"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["otp_code"], "123456")

    def test_empty_otp(self):
        form = ValidateOTPForm(data={"otp_code": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("otp_code", form.errors)

    def test_otp_too_long(self):
        form = ValidateOTPForm(data={"otp_code": "1" * 16})  
        self.assertFalse(form.is_valid())
        self.assertIn("otp_code", form.errors)


class CardFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="carduser", password="Pass123!")
        self.wallet = Wallet.objects.create(user=self.user)

    def test_valid_card(self):
        data = {
            "card_number": "6037991234567890",
            "cvv2": "123",
            "month": "09",
            "day": "15",
        }
        form = CardForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_cvv2_4_digits(self):
        data = {
            "card_number": "6037991234567890",
            "cvv2": "1234",
            "month": "12",
            "day": "31",
        }
        form = CardForm(data=data)
        self.assertTrue(form.is_valid())

    def test_card_number_wrong_length(self):
        data = {
            "card_number": "12345",
            "cvv2": "123",
            "month": "09",
            "day": "15",
        }
        form = CardForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("card_number", form.errors)

    def test_card_number_non_digit(self):
        data = {
            "card_number": "60379912345678ab",
            "cvv2": "123",
            "month": "09",
            "day": "15",
        }
        form = CardForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("card_number", form.errors)

    def test_invalid_cvv2(self):
        
        form = CardForm(data={
            "card_number": "6037991234567890",
            "cvv2": "12",
            "month": "09",
            "day": "15",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("cvv2", form.errors)

        # شامل حرف
        form = CardForm(data={
            "card_number": "6037991234567890",
            "cvv2": "12a",
            "month": "09",
            "day": "15",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("cvv2", form.errors)

    def test_invalid_month(self):
        invalid_months = ["00", "13", "99", "5", "1"]  
        for m in invalid_months:
            form = CardForm(data={
                "card_number": "6037991234567890",
                "cvv2": "123",
                "month": m,
                "day": "15",
            })
            self.assertFalse(form.is_valid(), f"month={m} should be invalid")
            self.assertIn("month", form.errors)

    def test_invalid_day(self):
        invalid_days = ["00", "32", "99", "5", "1"]
        for d in invalid_days:
            form = CardForm(data={
                "card_number": "6037991234567890",
                "cvv2": "123",
                "month": "09",
                "day": d,
            })
            self.assertFalse(form.is_valid(), f"day={d} should be invalid")
            self.assertIn("day", form.errors)

    def test_missing_fields(self):
        form = CardForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("card_number", form.errors)
        self.assertIn("cvv2", form.errors)
        self.assertIn("month", form.errors)
        self.assertIn("day", form.errors)

    def test_save_with_wallet(self):
        data = {
            "card_number": "6037991234567890",
            "cvv2": "456",
            "month": "12",
            "day": "31",
        }
        form = CardForm(data=data)
        self.assertTrue(form.is_valid())
        card = form.save(commit=False)
        card.wallet = self.wallet
        card.save()
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(card.wallet, self.wallet)