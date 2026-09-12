from django.urls import path, include
from .views import *

urlpatterns = [
    path("login/", LogingView.as_view(), name="login"),
    path("logout/", LogingoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("forget_password/", ForgetPasswordView.as_view(), name="forget_password"),
    path("validate_otp/", ValidateOtpView.as_view(), name="validate_otp"),
    path("profile/", Profile.as_view(), name="profile"),
    path("profile/wallet", Walletview.as_view(), name="wallet"),
    path("profile/wallet/charge", ChargeWalletView.as_view(), name="charge"),
    path(
        "contact_send_mail/", SendEmailContactView.as_view(), name="contact_send_mail"
    ),
    path("", include("allauth.urls")),
]
