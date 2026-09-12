
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from accounts.views import (
    LogingView,
    LogingoutView,
    RegisterView,
    ChangePasswordView,
    ForgetPasswordView,
    ValidateOtpView,
    Profile,
    Walletview,
    CardListView,
    CreateCardView,
    ChargeWalletView,
    EditCardView,
    RemoveCardView,
)


class AccountsURLTest(SimpleTestCase):

    def test_login_url(self):
        url = reverse("login")

        self.assertEqual(url, "/accounts/login/")
        self.assertEqual(
            resolve(url).func.view_class,
            LogingView,
        )

    def test_logout_url(self):
        url = reverse("logout")

        self.assertEqual(url, "/accounts/logout/")
        self.assertEqual(
            resolve(url).func.view_class,
            LogingoutView,
        )

    def test_register_url(self):
        url = reverse("register")

        self.assertEqual(url, "/accounts/register/")
        self.assertEqual(
            resolve(url).func.view_class,
            RegisterView,
        )

    def test_change_password_url(self):
        url = reverse("change_password")

        self.assertEqual(
            url,
            "/accounts/change_password/",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            ChangePasswordView,
        )

    def test_forget_password_url(self):
        url = reverse("forget_password")

        self.assertEqual(
            url,
            "/accounts/forget_password/",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            ForgetPasswordView,
        )

    def test_validate_otp_url(self):
        url = reverse("validate_otp")

        self.assertEqual(
            url,
            "/accounts/validate_otp/",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            ValidateOtpView,
        )

    def test_profile_url(self):
        url = reverse("profile")

        self.assertEqual(
            url,
            "/accounts/profile/",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            Profile,
        )

    def test_wallet_url(self):
        url = reverse("wallet")

        self.assertEqual(
            url,
            "/accounts/profile/wallet",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            Walletview,
        )

    def test_my_cards_url(self):
        url = reverse("mycards")

        self.assertEqual(
            url,
            "/accounts/profile/wallet/mycards",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            CardListView,
        )

    def test_create_card_url(self):
        url = reverse("card")

        self.assertEqual(
            url,
            "/accounts/profile/wallet/card",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            CreateCardView,
        )

    def test_charge_wallet_url(self):
        url = reverse("charge")

        self.assertEqual(
            url,
            "/accounts/profile/wallet/charge",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            ChargeWalletView,
        )

    def test_edit_card_url(self):
        url = reverse("edit_card", kwargs={"pk": 10})

        self.assertEqual(
            url,
            "/accounts/profile/wallet/edit/10",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            EditCardView,
        )

    def test_delete_card_url(self):
        url = reverse("delete_card", kwargs={"pk": 10})

        self.assertEqual(
            url,
            "/accounts/profile/wallet/delete/10",
        )
        self.assertEqual(
            resolve(url).func.view_class,
            RemoveCardView,
        )
