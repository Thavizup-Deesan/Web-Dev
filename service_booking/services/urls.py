# services/urls.py
from django.urls import path
from .views import (
    AdminLoginView,
    HomeView,
    TableBrowseView,
    # Admin Views
    TableListView,
    TableCreateView,
    TableUpdateView,
    TableDeleteView,
    # User Views
    BookingCreateView,
    BookingSuccessView,
    BookingHistoryView,
    BookingUpdateView,
    BookingDeleteView,
    AdminDashboardView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),

    path('manage/login/', AdminLoginView.as_view(), name='admin_login'),
    path('manage/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),

    path('manage/tables/', TableListView.as_view(), name='table_list'),
    path('manage/tables/new/', TableCreateView.as_view(), name='table_create'),
    path('manage/tables/<int:pk>/edit/', TableUpdateView.as_view(), name='table_update'),
    path('manage/tables/<int:pk>/delete/', TableDeleteView.as_view(), name='table_delete'),

    path('booking/new/', BookingCreateView.as_view(), name='booking_create'),
    path('booking/success/', BookingSuccessView.as_view(), name='booking_success'),
    path('booking/history/', BookingHistoryView.as_view(), name='booking_history'),
    path('booking/<int:pk>/edit/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking/<int:pk>/cancel/', BookingDeleteView.as_view(), name='booking_cancel'),
    path('tables/', TableBrowseView.as_view(), name='table_browse'), 
]