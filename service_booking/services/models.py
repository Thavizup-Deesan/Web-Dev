# services/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser

# 1. เปลี่ยนจาก Service เป็น Table
class Table(models.Model):
    table_number = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField(help_text="จำนวนที่นั่ง")
    description = models.TextField(blank=True, null=True, help_text="รายละเอียดเพิ่มเติม เช่น 'โต๊ะริมหน้าต่าง'")

    def __str__(self):
        return f"โต๊ะ {self.table_number} ({self.capacity} ที่นั่ง)"

# 2. ปรับแก้ Booking Model
class Booking(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    # เปลี่ยนจาก service เป็น table
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE) 
    
    booking_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        # ป้องกันการจองโต๊ะซ้ำในเวลาเดียวกัน
        unique_together = ('table', 'booking_datetime')

    def __str__(self):
        return f"การจองโต๊ะ {self.table.table_number} โดยคุณ {self.user.username} วันที่ {self.booking_datetime.strftime('%d/%m/%y %H:%M')}"

    # เมธอดสำหรับเช็คว่าสามารถแก้ไข/ยกเลิกได้หรือไม่ (ก่อนเวลาจอง 2 ชั่วโมง)
    def can_be_modified(self):
        return timezone.now() < self.booking_datetime - timedelta(hours=2)