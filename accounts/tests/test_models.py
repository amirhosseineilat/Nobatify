
from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from accounts.models import CustomUser, Wallet, Otp, Card


class CustomUserModelTest(TestCase):

    def test_create_user(self):

        user = CustomUser.objects.create_user(
            username="amir",
            email="amir@example.com",
            password="12345678",
        )

        saved_user = CustomUser.objects.get(id=user.id)

        self.assertEqual(saved_user.username, "amir")
        self.assertEqual(saved_user.email, "amir@example.com")
        self.assertTrue(saved_user.check_password("12345678"))

    def test_user_str(self):

        user = CustomUser.objects.create_user(
            username="amir",
            email="amir@example.com",
            password="12345678",
        )

        self.assertEqual(str(user), "amir")

    def test_email_is_unique(self):

        CustomUser.objects.create_user(
            username="amir",
            email="amir@example.com",
            password="12345678",
        )

        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username="amir2",
                email="amir@example.com",
                password="12345678",
            )


class WalletModelTest(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="amir",
            email="amir@example.com",
            password="12345678",
        )

    def test_create_wallet(self):
        """
        تست ساخت Wallet
        """

        wallet = Wallet.objects.create(
            user=self.user
        )

        self.assertEqual(wallet.user, self.user)
        self.assertEqual(wallet.balance, 0)

    def test_wallet_default_balance(self):

        wallet = Wallet.objects.create(
            user=self.user
        )

        self.assertEqual(wallet.balance, 0)

    def test_wallet_str(self):

        wallet = Wallet.objects.create(
            user=self.user
        )

        self.assertEqual(str(wallet), "amir's Wallet")

    def test_wallet_user_is_one_to_one(self):

        Wallet.objects.create(
            user=self.user
        )

        with self.assertRaises(Exception):
            Wallet.objects.create(
                user=self.user
            )


class OtpModelTest(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="amir",
            email="amir@example.com",
            password="12345678",
        )

    def test_generate_otp(self):

        otp = Otp()

        code = otp.generate_otp(
            user=self.user,
            purpose="login",
        )

        # کد OTP باید ۶ رقم باشد
        self.assertEqual(len(code), 6)

        # باید فقط شامل عدد باشد
        self.assertTrue(code.isdigit())

        # OTP باید در دیتابیس ذخیره شده باشد
        saved_otp = Otp.objects.get(id=otp.id)

        self.assertEqual(saved_otp.user, self.user)
        self.assertEqual(saved_otp.purpose, "login")
        self.assertEqual(saved_otp.code, code)

    def test_otp_is_unused_by_default(self):

        otp = Otp.objects.create(
            user=self.user,
            code="123456",
            expire_time=now() + timedelta(minutes=2),
            purpose="login",
        )

        self.assertFalse(otp.is_used)

    def test_otp_expire_time(self):

        before = now()

        otp = Otp()
        otp.generate_otp(
            user=self.user,
            purpose="login",
        )

        after = now()

        self.assertGreaterEqual(
            otp.expire_time,
            before + timedelta(minutes=2),
        )

        self.assertLessEqual(
            otp.expire_time,
            after + timedelta(minutes=2),
        )

    def test_otp_str_unused(self):

        otp = Otp.objects.create(
            user=self.user,
            code="123456",
            expire_time=now() + timedelta(minutes=2),
            purpose="login",
        )

        self.assertEqual(
            str(otp),
            "OTP for amir - Unused",
        )

    def test_otp_str_used(self):

        otp = Otp.objects.create(
            user=self.user,
            code="123456",
            expire_time=now() + timedelta(minutes=2),
            purpose="login",
            is_used=True,
        )

        self.assertEqual(
            str(otp),
            "OTP for amir - Used",
        )


class CardModelTest(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="amir",
            email="amir@example.com",
            password="12345678",
        )

        self.wallet = Wallet.objects.create(
            user=self.user
        )

    def test_create_card(self):

        card = Card.objects.create(
            card_number="1234567812345678",
            cvv2="123",
            month="12",
            day="25",
            wallet=self.wallet,
        )

        self.assertEqual(
            card.card_number,
            "1234567812345678",
        )

        self.assertEqual(card.cvv2, "123")
        self.assertEqual(card.month, "12")
        self.assertEqual(card.day, "25")
        self.assertEqual(card.wallet, self.wallet)

    def test_card_belongs_to_wallet(self):

        card = Card.objects.create(
            card_number="1234567812345678",
            cvv2="123",
            month="12",
            day="25",
            wallet=self.wallet,
        )

        self.assertEqual(card.wallet, self.wallet)

    def test_multiple_cards_for_one_wallet(self):

        card1 = Card.objects.create(
            card_number="1111111111111111",
            cvv2="123",
            month="12",
            day="25",
            wallet=self.wallet,
        )

        card2 = Card.objects.create(
            card_number="2222222222222222",
            cvv2="456",
            month="10",
            day="30",
            wallet=self.wallet,
        )

        self.assertEqual(self.wallet.card.count(), 2)

        self.assertIn(card1, self.wallet.card.all())
        self.assertIn(card2, self.wallet.card.all())
