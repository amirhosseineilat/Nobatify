from django.forms import ModelForm, CharField, Form
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    SetPasswordForm,
)
from django.contrib.auth import get_user_model
from .models import Card , Wallet

User = get_user_model()

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "first_name",
            "last_name",
        ]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class ForgetForm(ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ValidateOTPForm(Form):
    otp_code = CharField(required=True, max_length=15)


class CardForm(ModelForm):
    class meta:
        model = Card
        fields = ['card_number','cvv2','month','day']

