from django.urls import path
from .views import log_list, export_logs

urlpatterns = [
    path('', log_list, name='log_list'),
    path('logs/export/', export_logs, name='export_logs'),
]
