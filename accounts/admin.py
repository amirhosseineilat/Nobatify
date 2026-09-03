from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Wallet, Otp, CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "is_staff", "is_active", "is_admin")
    list_filter = ("is_staff", "is_active", "is_admin")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_admin")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_active", "is_admin"),
        }),
    )
    search_fields = ("username", "email")
    ordering = ("username",)
    
    
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
