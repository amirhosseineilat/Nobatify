from django.db import models
from doctors.models import Doctor
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.core.validators import MinValueValidator
from django_jalali.db import models as jmodels

User = get_user_model()
# Create your models here.

class TimeSlot(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="time_slots"
    )
    date = jmodels.jDateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text='Consultation fee for this time slot (Tomans or Rials)'
    )
    is_reserved = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "date", "start_time"], name="unique_doctor_timeslot"
            )
        ]

        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.doctor} - {self.date} ({self.start_time} - {self.end_time}) | {self.price}"


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
    
    paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="The payment amount recorded at the time of booking"
    )


    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.paid is None and self.time_slot:
            self.paid = self.time_slot.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.time_slot} | Fee: {self.paid}"
        
