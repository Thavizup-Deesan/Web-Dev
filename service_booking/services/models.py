# service/models.py
from django.db import models
from accounts.models import CustomUser


# 2. Service Model (ที่คุณสร้างไว้แล้ว)
class Service(models.Model):
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.service_name

# 3. Booking Model
class Booking(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    # Foreign Key ไปยัง CustomUser และ Service
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    booking_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.service.service_name} for {self.user.username} at {self.booking_datetime}"