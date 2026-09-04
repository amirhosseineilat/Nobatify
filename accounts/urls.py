from django.urls import path,include
from .views import *




urlpatterns = [
    path("login/", LogingView.as_view(), name="login"),
    path("logout/", LogingoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("forget_password/", ForgetPasswordView.as_view(), name="forget_password"),
    path("validate_otp/", ValidateOtpView.as_view(), name="validate_otp"),
    path("profile/", Profile.as_view(), name="profile"),
    path("profile/wallet/", Wallet.as_view(), name="wallet"),
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path("profile/wallet", Walletview.as_view(), name="wallet"),
    path("profile/wallet/mycards", CardListView.as_view(), name="mycards"),
    path("profile/wallet/card", CreateCardView.as_view(), name="card"),
    path("profile/wallet/charge", ChargeWalletView.as_view(), name="charge"),
    path("profile/wallet/edit/<int:pk>", EditCardView.as_view(), name="edit_card"),
    path("profile/wallet/delete/<int:pk>", RemoveCardView.as_view(), name="delete_card"),
    path("",include("allauth.urls"))
]
