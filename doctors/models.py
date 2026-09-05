from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Speciality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    specialities = models.ManyToManyField(Speciality, related_name="doctors")
    birth_date = models.DateField()
    medical_license_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=8)
    address = models.TextField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def average_rating(self):
        result = self.comments.aggregate(avg=models.Avg("rating"))
        return round(result["avg"] or 0, 1)

    @property
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=5
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.first_name} {self.user.last_name} on {self.doctor.first_name} {self.doctor.last_name}"


