# services/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from .models import Table, Booking
from .forms import BookingForm, TableForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models import Count

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'admin_login'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'admin'

class HomeView(TemplateView):
    model = Table
    template_name = 'homepage.html'
    context_object_name = 'tables'

class TableBrowseView(ListView):
    model = Table
    template_name = 'services/table_browse.html'
    context_object_name = 'tables'
    ordering = ['table_number']

class TableListView(AdminRequiredMixin, ListView):
    model = Table
    template_name = 'services/table_list.html'
    context_object_name = 'tables'

class TableCreateView(AdminRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = 'services/table_form.html'
    success_url = reverse_lazy('table_list')

class TableUpdateView(AdminRequiredMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'services/table_form.html'
    success_url = reverse_lazy('table_list')

class TableDeleteView(AdminRequiredMixin, DeleteView):
    model = Table
    template_name = 'services/table_confirm_delete.html'
    success_url = reverse_lazy('table_list')

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'services/booking_form.html'
    success_url = reverse_lazy('booking_success')

    def get_initial(self):
        initial = super().get_initial()
        table_id = self.request.GET.get('table')
        if table_id:
            initial['table'] = table_id
        return initial

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
    template_name = 'services/booking_cancel.html'
    success_url = reverse_lazy('booking_history')

    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.user and booking.can_be_modified()

    def handle_no_permission(self):
        messages.error(self.request, "คุณไม่สามารถยกเลิกการจองนี้ได้ (อาจจะเลยเวลาที่กำหนด)")
        return redirect('booking_history')

class AdminLoginView(LoginView):
    template_name = 'registration/admin_login.html'
    redirect_authenticated_user = True 

    def get_success_url(self):
        return reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        user = form.get_user()
        if user.role == 'admin' or user.is_superuser:
            messages.success(self.request, f"ยินดีต้อนรับกลับมา, {user.username}!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "บัญชีนี้ไม่มีสิทธิ์เข้าถึงส่วนผู้ดูแลระบบ")
            return self.form_invalid(form)

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'services/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['bookings'] = Booking.objects.filter(
            status='confirmed',
            booking_datetime__gte=today
        ).order_by('booking_datetime')

        bookings_daily = Booking.objects.filter(status='confirmed') \
            .annotate(day=TruncDate('booking_datetime')) \
            .values('day') \
            .annotate(count=Count('id')) \
            .order_by('day')
        line_labels = [b['day'].strftime('%Y-%m-%d') for b in bookings_daily]
        line_data = [b['count'] for b in bookings_daily]
        context['line_labels'] = line_labels
        context['line_data'] = line_data

        pie_data = Booking.objects.filter(status='confirmed') \
            .values('table__is_outdoor') \
            .annotate(count=Count('id'))
        pie_labels = ["Outdoor" if p['table__is_outdoor'] else "Indoor" for p in pie_data]
        pie_values = [p['count'] for p in pie_data]
        context['pie_labels'] = pie_labels
        context['pie_values'] = pie_values

        return context
    
