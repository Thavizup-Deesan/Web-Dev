# services/forms.py
from django import forms
from .models import Booking, Table

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['table', 'booking_datetime', 'notes']
        widgets = {
            'table': forms.Select(attrs={'class': 'block w-full px-3 py-3 border border-gray-300 text-black rounded-lg'}),
            'booking_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'block w-full px-3 py-3 border border-gray-300 text-black rounded-lg'}
            ),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'block w-full px-3 py-3 border border-gray-300 text-black rounded-lg', 'placeholder': 'คำขอพิเศษ (ถ้ามี)'}),
        }
        labels = {
            'table': 'เลือกโต๊ะ',
            'booking_datetime': 'เลือกวันและเวลา',
            'notes': 'หมายเหตุ',
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        booking_datetime = cleaned_data.get("booking_datetime")

        if table and booking_datetime:

            queryset = Booking.objects.filter(table=table, booking_datetime=booking_datetime)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError("โต๊ะนี้ถูกจองแล้วในเวลาที่คุณเลือก กรุณาเลือกเวลาอื่น")
        
        return cleaned_data
    
class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['table_number', 'capacity', 'is_outdoor', 'description', 'image']
        widgets = {
            'table_number': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 text-black focus:border-indigo-500'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 text-black focus:border-indigo-500'
            }),
            'is_outdoor': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 border-gray-300 rounded text-black focus:ring-indigo-500'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 text-black focus:border-indigo-500'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
        }
        labels = {
            'table_number': 'หมายเลขโต๊ะ',
            'capacity': 'จำนวนที่นั่ง',
            'is_outdoor': 'เป็นโต๊ะโซน Outdoor',
            'description': 'รายละเอียดเพิ่มเติม',
        }
