# services/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView , TemplateView
from django.urls import reverse_lazy
from .models import Service
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'admin'
    
class HomeView(TemplateView):
    template_name = 'homepage.html'

class ServiceListView(AdminRequiredMixin, ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'

class ServiceCreateView(AdminRequiredMixin, CreateView):
    model = Service
    fields = ['service_name', 'description', 'duration_minutes', 'price']
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('service_list')

class ServiceUpdateView(AdminRequiredMixin, UpdateView):
    model = Service
    fields = ['service_name', 'description', 'duration_minutes', 'price']
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('service_list')

class ServiceDeleteView(AdminRequiredMixin, DeleteView):
    model = Service
    template_name = 'services/service_confirm_delete.html'
    success_url = reverse_lazy('service_list')