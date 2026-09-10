from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from accounts.models import Wallet, Card

User = get_user_model()


class AccountViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ali",
            email="ali@example.com",
            password="StrongPassword123",
            first_name="Ali",
            last_name="Asghar",
        )

        self.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="StrongPassword123",
        )

        self.wallet = Wallet.objects.create(
            user=self.user,
            balance=Decimal("100000.00"),
        )

        self.card = Card.objects.create(
            wallet=self.wallet,
            card_number="1234567812345678",
            cvv2="123",
            month="12",
            day="30",
        )

    def login(self):
        self.client.login(
            username="ali",
            password="StrongPassword123",
        )

    def test_login_get(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_success(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "ali",
                "password": "StrongPassword123",
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any(str(message) == "ورود با موفقیت انجام شد" for message in messages)
        )

    def test_login_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "ali",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_register_get(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_register_success(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "first_name": "New",
                "last_name": "User",
            },
        )

        self.assertRedirects(response, reverse("login"))

        self.assertTrue(
            User.objects.filter(
                username="newuser",
                email="new@example.com",
            ).exists()
        )

    def test_register_invalid_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "StrongPassword123",
                "password2": "WrongPassword123",
                "first_name": "New",
                "last_name": "User",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_change_password_without_verification(self):
        response = self.client.get(reverse("change_password"))

        self.assertRedirects(
            response,
            reverse("forget_password"),
        )

    def test_change_password_without_user_id(self):
        session = self.client.session

        session["reset_verified"] = True
        session.save()

        response = self.client.get(reverse("change_password"))

        self.assertRedirects(
            response,
            reverse("forget_password"),
        )

    def test_change_password_expired_session(self):
        session = self.client.session

        session["reset_verified"] = True
        session["reset_user_id"] = self.user.id
        session["rest_expire_time"] = now().timestamp() - 10

        session.save()

        response = self.client.get(reverse("change_password"))

        self.assertRedirects(
            response,
            reverse("forget_password"),
        )

        session = self.client.session

        self.assertNotIn("reset_verified", session)
        self.assertNotIn("reset_user_id", session)
        self.assertNotIn("rest_expire_time", session)

    def test_change_password_get(self):
        session = self.client.session

        session["reset_verified"] = True
        session["reset_user_id"] = self.user.id
        session["rest_expire_time"] = now().timestamp() + 120

        session.save()

        response = self.client.get(reverse("change_password"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/change_password.html",
        )

    def test_change_password_success(self):
        session = self.client.session

        session["reset_verified"] = True
        session["reset_user_id"] = self.user.id
        session["rest_expire_time"] = now().timestamp() + 120

        session.save()

        response = self.client.post(
            reverse("change_password"),
            {
                "new_password1": "NewStrongPassword123",
                "new_password2": "NewStrongPassword123",
            },
        )

        self.assertRedirects(
            response,
            reverse("login"),
        )

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password("NewStrongPassword123"))

        session = self.client.session

        self.assertNotIn("reset_verified", session)
        self.assertNotIn("reset_user_id", session)
        self.assertNotIn("rest_expire_time", session)

    def test_forget_password_get(self):
        response = self.client.get(reverse("forget_password"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/forget_password.html",
        )

    def test_validate_otp_get(self):
        response = self.client.get(reverse("validate_otp"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/validate_otp.html",
        )

    @patch("accounts.views.AccountService.validate_otp")
    def test_validate_otp_success(
        self,
        mock_validate_otp,
    ):
        mock_validate_otp.return_value = (
            True,
            self.user,
        )

        response = self.client.post(
            reverse("validate_otp"),
            {
                "otp_code": "123456",
            },
        )

        self.assertRedirects(
            response,
            reverse("change_password"),
        )

        mock_validate_otp.assert_called_once_with(
            response.wsgi_request,
            "123456",
            "password_reset",
        )

        session = self.client.session

        self.assertEqual(
            session["reset_user_id"],
            self.user.id,
        )

        self.assertTrue(session["reset_verified"])

        self.assertIn(
            "rest_expire_time",
            session,
        )

    @patch("accounts.views.AccountService.validate_otp")
    def test_validate_otp_failure(
        self,
        mock_validate_otp,
    ):
        mock_validate_otp.return_value = (
            False,
            None,
        )

        response = self.client.post(
            reverse("validate_otp"),
            {
                "otp_code": "123456",
            },
        )

        self.assertRedirects(
            response,
            reverse("forget_password"),
        )

    def test_validate_otp_empty(self):
        response = self.client.post(
            reverse("validate_otp"),
            {
                "otp_code": "",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
        )

    def test_profile(self):
        self.login()

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/profile.html",
        )

        self.assertEqual(
            response.context["user"],
            self.user,
        )

    def test_wallet_requires_login(self):
        response = self.client.get(reverse("wallet"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('wallet')}",
        )

    def test_wallet(self):
        self.login()

        response = self.client.get(reverse("wallet"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/wallet.html",
        )

        self.assertEqual(
            response.context["wallet"],
            self.wallet,
        )

    def test_wallet_creates_wallet(self):
        self.wallet.delete()

        self.login()

        response = self.client.get(reverse("wallet"))

        self.assertEqual(response.status_code, 200)

        wallet = Wallet.objects.get(user=self.user)

        self.assertEqual(
            response.context["wallet"],
            wallet,
        )

        self.assertEqual(
            wallet.balance,
            Decimal("0.00"),
        )

    def test_card_list_requires_login(self):
        response = self.client.get(reverse("mycards"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('mycards')}",
        )

    def test_card_list(self):
        self.login()

        response = self.client.get(reverse("mycards"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/mycard.html",
        )

        self.assertIn(
            self.card,
            response.context["cards"],
        )

    def test_create_card_get(self):
        self.login()

        response = self.client.get(reverse("card"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/createcard.html",
        )

    def test_create_card_success(self):
        self.login()

        response = self.client.post(
            reverse("card"),
            {
                "card_number": "1111222233334444",
                "cvv2": "456",
                "month": "10",
                "day": "25",
            },
        )

        self.assertRedirects(
            response,
            reverse("mycards"),
        )

        self.assertTrue(
            Card.objects.filter(
                wallet=self.wallet,
                card_number="1111222233334444",
            ).exists()
        )

    def test_create_card_invalid_number(self):
        self.login()

        response = self.client.post(
            reverse("card"),
            {
                "card_number": "1234",
                "cvv2": "456",
                "month": "10",
                "day": "25",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(Card.objects.filter(card_number="1234").exists())

    def test_create_card_creates_wallet(self):
        self.wallet.delete()

        self.login()

        response = self.client.post(
            reverse("card"),
            {
                "card_number": "1111222233334444",
                "cvv2": "456",
                "month": "10",
                "day": "25",
            },
        )

        self.assertRedirects(
            response,
            reverse("mycards"),
        )

        wallet = Wallet.objects.get(user=self.user)

        self.assertTrue(
            Card.objects.filter(
                wallet=wallet,
                card_number="1111222233334444",
            ).exists()
        )

    def test_edit_card_get(self):
        self.login()

        response = self.client.get(
            reverse(
                "edit_card",
                kwargs={"pk": self.card.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/createcard.html",
        )

    def test_edit_card_success(self):
        self.login()

        response = self.client.post(
            reverse(
                "edit_card",
                kwargs={"pk": self.card.pk},
            ),
            {
                "card_number": "9999888877776666",
                "cvv2": "789",
                "month": "11",
                "day": "20",
            },
        )

        self.assertRedirects(
            response,
            reverse("mycards"),
        )

        self.card.refresh_from_db()

        self.assertEqual(
            self.card.card_number,
            "9999888877776666",
        )

        self.assertEqual(
            self.card.cvv2,
            "789",
        )

    def test_edit_other_user_card(self):
        other_wallet = Wallet.objects.create(
            user=self.other_user,
            balance=Decimal("50000.00"),
        )

        other_card = Card.objects.create(
            wallet=other_wallet,
            card_number="5555666677778888",
            cvv2="111",
            month="01",
            day="01",
        )

        self.login()

        response = self.client.get(
            reverse(
                "edit_card",
                kwargs={"pk": other_card.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_delete_card(self):
        self.login()

        card_id = self.card.pk

        response = self.client.post(
            reverse(
                "delete_card",
                kwargs={"pk": card_id},
            )
        )

        self.assertRedirects(
            response,
            reverse("mycards"),
        )

        self.assertFalse(Card.objects.filter(pk=card_id).exists())

    def test_delete_other_user_card(self):
        other_wallet = Wallet.objects.create(
            user=self.other_user,
            balance=Decimal("50000.00"),
        )

        other_card = Card.objects.create(
            wallet=other_wallet,
            card_number="5555666677778888",
            cvv2="111",
            month="01",
            day="01",
        )

        self.login()

        response = self.client.post(
            reverse(
                "delete_card",
                kwargs={"pk": other_card.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse("mycards"),
        )

        self.assertFalse(Card.objects.filter(pk=other_card.pk).exists())

    def test_charge_wallet_get(self):
        self.login()

        response = self.client.get(reverse("charge"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/chargewallet.html",
        )

        self.assertEqual(
            response.context["wallet"],
            self.wallet,
        )

        self.assertIn(
            self.card,
            response.context["cards"],
        )

    def test_charge_wallet(self):
        self.login()

        response = self.client.post(
            reverse("charge"),
            {
                "balance": "25000",
            },
        )

        self.assertRedirects(
            response,
            reverse("wallet"),
        )

        self.wallet.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("125000.00"),
        )

    def test_charge_wallet_zero(self):
        self.login()

        response = self.client.post(
            reverse("charge"),
            {
                "balance": "0",
            },
        )

        self.assertRedirects(
            response,
            reverse("wallet"),
        )

        self.wallet.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("100000.00"),
        )

    def test_home(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
