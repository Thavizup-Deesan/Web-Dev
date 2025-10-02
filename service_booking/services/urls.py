# services/urls.py
from django.urls import path
from .views import (
    HomeView,
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
)

urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),

    # URL สำหรับ Admin จัดการโต๊ะ
    path('manage/tables/', TableListView.as_view(), name='table_list'),
    path('manage/tables/new/', TableCreateView.as_view(), name='table_create'),
    path('manage/tables/<int:pk>/edit/', TableUpdateView.as_view(), name='table_update'),
    path('manage/tables/<int:pk>/delete/', TableDeleteView.as_view(), name='table_delete'),

    # URL สำหรับ User จัดการการจอง
    path('booking/new/', BookingCreateView.as_view(), name='booking_create'),
    path('booking/success/', BookingSuccessView.as_view(), name='booking_success'),
    path('booking/history/', BookingHistoryView.as_view(), name='booking_history'),
    path('booking/<int:pk>/edit/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking/<int:pk>/cancel/', BookingDeleteView.as_view(), name='booking_cancel'), # ใช้ BookingDeleteView
]