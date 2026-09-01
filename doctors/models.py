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
    
    @property
    def average_rating(self):
        result = self.comments.aggregate(avg=models.Avg('rating'))
        return round(result['avg'] or 0 , 1)
    
    @property
    def comment_count(self):
        return self.comments.count()
    

class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
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
    
    
    
    
class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_reserved = models.BooleanField(default=False) 
    
    # class Meta:
    #     unique_together = ('doctor', 'date', 'start_time')
    #     ordering = ['date', 'start_time']
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'start_time'],
                name='unique_doctor_timeslot'
            )
        ]

        ordering = ['date', 'start_time']
        
    def __str__(self):
        return f"{self.doctor} - {self.date} ({self.start_time} - {self.end_time})"