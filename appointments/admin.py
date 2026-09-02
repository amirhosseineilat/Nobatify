from django.contrib import admin
from .models import Appointment


# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("doctor", "patient", "time_slot", "status", "created_at")
    search_fields = ("doctor__first_name", "doctor__last_name", "patient__username")
    list_filter = ("status", "created_at")
