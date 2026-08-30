from django.urls import path

urlpatterns = [
    path("login/", name="login"),
    path("register/", name="register"),
    path("change_password/", name="change_password"),
    path("profile/", name="profile"),
    path("profile/wallet", name="wallet"),
]
