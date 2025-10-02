# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('ข้อมูลเพิ่มเติม', {'fields': ('full_name', 'phone_number', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('full_name', 'phone_number', 'role')}),
    )
    list_display = ['username', 'email', 'full_name', 'role', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)