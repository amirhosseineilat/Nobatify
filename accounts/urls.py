from django.urls import path
from .views import *

app_name = 'accounts' 


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
]
