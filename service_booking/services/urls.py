from django.urls import path
from .views import ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('new/', ServiceCreateView.as_view(), name='service_new'),
    path('<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_edit'),
    path('<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
]