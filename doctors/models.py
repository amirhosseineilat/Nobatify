from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    rating = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.first_name} {self.user.last_name} on {self.doctor.first_name} {self.doctor.last_name}"

class Speciality(models.Model):
    doctor = models.ManyToManyField(Doctor, related_name='specialities')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name