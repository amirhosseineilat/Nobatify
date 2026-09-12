from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels

User = get_user_model()
# Create your models here.


class TransActoin(models.Model):
    PURPOSE = (
        ("wallet_charge", "Charge Wallet"),
        ("appointment", "Appointment"),
    )

    user = models.ForeignKey(User, on_delete=models.Case, related_name="transactions")
    porpuse = models.CharField(choices=PURPOSE)
    amount = models.FloatField()
    authority = models.CharField()
    card_number = models.CharField(null=True, blank=True)
    creted_at = jmodels.jDateTimeField(auto_now_add=True)
    fee = models.IntegerField(null=True, blank=True)
