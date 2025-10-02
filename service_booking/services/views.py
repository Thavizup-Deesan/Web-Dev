# services/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import Table, Booking  # เปลี่ยนจาก Service เป็น Table
from .forms import BookingForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.utils import timezone

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'admin'

class HomeView(TemplateView):
    template_name = 'homepage.html'

# --- Admin Views (จัดการโต๊ะ) ---
class TableListView(AdminRequiredMixin, ListView):
    model = Table
    template_name = 'services/table_list.html' # เปลี่ยนชื่อ template
    context_object_name = 'tables'

class TableCreateView(AdminRequiredMixin, CreateView):
    model = Table
    fields = ['table_number', 'capacity','is_outdoor', 'description'] # เปลี่ยน fields
    template_name = 'services/table_form.html' # เปลี่ยนชื่อ template
    success_url = reverse_lazy('table_list')

class TableUpdateView(AdminRequiredMixin, UpdateView):
    model = Table
    fields = ['table_number', 'capacity', 'is_outdoor', 'description'] # เปลี่ยน fields
    template_name = 'services/table_form.html' # เปลี่ยนชื่อ template
    success_url = reverse_lazy('table_list')

class TableDeleteView(AdminRequiredMixin, DeleteView):
    model = Table
    template_name = 'services/table_confirm_delete.html' # เปลี่ยนชื่อ template
    success_url = reverse_lazy('table_list')

# --- User Views (จัดการการจอง) ---
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'services/booking_form.html'
    success_url = reverse_lazy('booking_success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookingSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'services/booking_success.html'

class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'services/booking_history.html'
    context_object_name = 'bookings'
    ordering = ['-booking_datetime']

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# --- เพิ่ม View สำหรับแก้ไขและยกเลิก ---
class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'services/booking_form.html'
    success_url = reverse_lazy('booking_history')

    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.user and booking.can_be_modified()
    
    def handle_no_permission(self):
        messages.error(self.request, "คุณไม่สามารถแก้ไขการจองนี้ได้ (อาจจะเลยเวลาที่กำหนด)")
        return redirect('booking_history')

class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'services/booking_confirm_delete.html'
    success_url = reverse_lazy('booking_history')

    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.user and booking.can_be_modified()

    def handle_no_permission(self):
        messages.error(self.request, "คุณไม่สามารถยกเลิกการจองนี้ได้ (อาจจะเลยเวลาที่กำหนด)")
        return redirect('booking_history')
    
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'services/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ดึงข้อมูลการจองที่ยืนยันแล้ว และเป็นของวันนี้หรือในอนาคต
        today = timezone.now().date()
        context['bookings'] = Booking.objects.filter(
            status='confirmed',
            booking_datetime__gte=today
        ).order_by('booking_datetime')
        return context