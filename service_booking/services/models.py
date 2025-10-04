# services/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser

class Table(models.Model):
    table_number = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField(help_text="จำนวนที่นั่ง")

    is_outdoor = models.BooleanField(default=False, help_text="ติ๊กถ้าเป็นโต๊ะโซน Outdoor")
    
    description = models.TextField(blank=True, null=True, help_text="รายละเอียดเพิ่มเติม เช่น 'โต๊ะริมหน้าต่าง'")

    image = models.ImageField(
        upload_to='table_images/', 
        blank=True, 
        null=True, 
        help_text="รูปภาพโต๊ะ"
    )


    def __str__(self):
        zone = "Outdoor" if self.is_outdoor else "Indoor"
        return f"โต๊ะ {self.table_number} ({self.capacity} ที่นั่ง, โซน {zone})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE) 
    
    booking_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('table', 'booking_datetime')

    def __str__(self):
        return f"การจองโต๊ะ {self.table.table_number} โดยคุณ {self.user.username} วันที่ {self.booking_datetime.strftime('%d/%m/%y %H:%M')}"

    def can_be_modified(self):
        return timezone.now() < self.booking_datetime - timedelta(hours=2)