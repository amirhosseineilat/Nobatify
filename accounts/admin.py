from django.contrib import admin
from .models import Wallet, Otp

# Register your models here.


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")
    search_fields = ("user__username",)
    list_filter = ("balance",)


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "is_used", "expire_time", "purpose")
    search_fields = ("user__username", "code")
    list_filter = ("is_used", "purpose")
