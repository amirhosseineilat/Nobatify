from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet"


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expire_time = models.DateTimeField()
    purpose = models.CharField(
        max_length=50,
        choices=[("login", "Login"), ("password_reset", "Password Reset")],
    )

    def generate_otp(self, user):
        import random

        self.user = user
        self.code = str(random.randint(100000, 999999))
        self.expire_time = self.created_at + timedelta(minutes=2)
        self.save()
        return self.code

    def __str__(self):
        return f"OTP for {self.user.username} - {'Used' if self.is_used else 'Unused'}"
