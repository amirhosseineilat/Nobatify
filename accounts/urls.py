from django.urls import path
from .views import *


urlpatterns = [
    path("login/",LogingView.as_view(), name="login"),
    path("register/",RegisterView.as_view(), name="register"),
    path("change_password/",ChangePasswordView.as_view(), name="change_password"),
    path("profile/",Profile.as_view(), name="profile"),
    path("profile/wallet",Wallet.as_view(), name="wallet"),
]
