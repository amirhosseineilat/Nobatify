from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, Wallet


@receiver(post_save, sender=CustomUser)
def create_user_wallet(sender, instance, created, **kwargs):
    Wallet.objects.get_or_create(user=instance)
