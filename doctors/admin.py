from django.contrib import admin
from .models import  Doctor, Comment, Speciality


# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("doctor", "user", "content", "created_at")
    search_fields = ("doctor__first_name", "doctor__last_name", "user__username")
    list_filter = ("created_at",)


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


