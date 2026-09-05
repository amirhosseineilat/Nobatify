from django.forms import ModelForm, CharField, Form
from django import forms
from django.core.validators import RegexValidator
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

        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "نام کاربری",
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "ایمیل",
            }),

            "first_name": forms.TextInput(attrs={
                "placeholder": "نام",
            }),

            "last_name": forms.TextInput(attrs={
                "placeholder": "نام خانوادگی",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].help_text = "Your password can’t be too similar..."
        self.fields["password2"].help_text = "Your password must contain at least 8 characters..."


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


class CardForm(forms.ModelForm):

    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        validators=[
            RegexValidator(
                regex=r'^\d{16}$',
                message='شماره کارت باید دقیقاً ۱۶ رقم باشد.'
            )
        ]
    )

    cvv2 = forms.CharField(
        min_length=3,
        max_length=4,
        validators=[
            RegexValidator(
                regex=r'^\d{3,4}$',
                message='CVV2 باید ۳ یا ۴ رقم باشد.'
            )
        ]
    )

    month = forms.CharField(
        max_length=2,
        min_length=2,
        validators=[
            RegexValidator(
                regex=r'^(0[1-9]|1[0-2])$',
                message='ماه باید بین 01 تا 12 باشد.'
            )
        ]
    )

    day = forms.CharField(
        max_length=2,
        min_length=2,
        validators=[
            RegexValidator(
                regex=r'^(0[1-9]|[12][0-9]|3[01])$',
                message='روز باید بین 01 تا 31 باشد.'
            )
        ]
    )

    class Meta:
        model = Card
        fields = [
            'card_number',
            'cvv2',
            'month',
            'day',
        ]

