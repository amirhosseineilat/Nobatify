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

    def __str__(self):
        return f"OTP for {self.user.username} - {'Used' if self.is_used else 'Unused'}"
