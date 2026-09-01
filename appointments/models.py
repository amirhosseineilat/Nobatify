from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار تایید"
        CONFIRMED = "confirmed", "تایید شده"
        CANCELLED = "cancelled", "لغو شده"
        COMPLETED = "completed", "انجام شده"
    doctor = models.ForeignKey(
        "doctors.Doctor", on_delete=models.CASCADE, related_name="appointments"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointments", null=True
    )
    # date = models.DateField()
    # time = models.TimeField()
    
    time_slot = models.OneToOneField('doctor.TimeSlote', on_delete=models.CASCADE, related_name='appointment')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
                              
    created_at = models.DateTimeField(auto_now_add=True)  
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.time_slot}"