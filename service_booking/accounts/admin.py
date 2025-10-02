# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # fieldsets คือการจัดกลุ่ม field ในหน้าแก้ไขข้อมูล
    # เราจะเพิ่มกลุ่ม "ข้อมูลเพิ่มเติม" เข้าไป
    fieldsets = UserAdmin.fieldsets + (
        ('ข้อมูลเพิ่มเติม', {'fields': ('full_name', 'phone_number', 'role')}),
    )
    # add_fieldsets คือการจัดกลุ่ม field ในหน้าสร้าง user ใหม่
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('full_name', 'phone_number', 'role')}),
    )
    # list_display คือคอลัมน์ที่จะแสดงในหน้ารวม user ทั้งหมด
    list_display = ['username', 'email', 'full_name', 'role', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)