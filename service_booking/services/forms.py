# services/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['table', 'booking_datetime', 'notes'] # เปลี่ยนจาก service เป็น table
        widgets = {
            'table': forms.Select(attrs={'class': 'block w-full px-3 py-3 border border-gray-300 rounded-lg'}),
            'booking_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'block w-full px-3 py-3 border border-gray-300 rounded-lg'}
            ),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'block w-full px-3 py-3 border border-gray-300 rounded-lg', 'placeholder': 'คำขอพิเศษ (ถ้ามี)'}),
        }
        labels = {
            'table': 'เลือกโต๊ะ',
            'booking_datetime': 'เลือกวันและเวลา',
            'notes': 'หมายเหตุ',
        }

    # เพิ่มการ validation เพื่อป้องกันการจองซ้ำ และให้ feedback ที่ดีกับผู้ใช้
    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        booking_datetime = cleaned_data.get("booking_datetime")

        if table and booking_datetime:
            # ไม่นับตัวเองในกรณีที่เป็นการแก้ไข
            queryset = Booking.objects.filter(table=table, booking_datetime=booking_datetime)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError("โต๊ะนี้ถูกจองแล้วในเวลาที่คุณเลือก กรุณาเลือกเวลาอื่น")
        
        return cleaned_data