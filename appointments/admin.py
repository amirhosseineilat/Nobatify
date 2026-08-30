from django.contrib import admin
from .models import Appointment


# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("doctor", "user", "date", "time", "created_at")
    search_fields = ("doctor__first_name", "doctor__last_name", "user__username")
    list_filter = ("date", "time")
