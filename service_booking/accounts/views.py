# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from accounts.models import CustomUser
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm, MyPasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView

class SignUpView(CreateView): 
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'registration/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    
class MyCustomPasswordResetView(PasswordResetView):
    form_class = MyPasswordResetForm
    