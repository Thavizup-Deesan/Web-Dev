# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm as MyPasswordResetForm

from services import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone_number')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('full_name', 'email', 'phone_number')

class MyPasswordResetForm(MyPasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'block w-full px-4 py-2 border border-gray-300 text-black rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500', 
        })