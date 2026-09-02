from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor, TimeSlot

# Create your models here.


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointments"
    )

    time_slot = models.OneToOneField(
        TimeSlot, on_delete=models.CASCADE, related_name="appointment"
    )
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointments"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.time_slot}"
