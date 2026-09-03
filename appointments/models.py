from django.db import models
from doctors.models import Doctor
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class TimeSlot(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="time_slots"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_reserved = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "date", "start_time"], name="unique_doctor_timeslot"
            )
        ]

        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.doctor} - {self.date} ({self.start_time} - {self.end_time})"

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
