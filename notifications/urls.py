from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.get_notifications, name='get_notifications'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
]