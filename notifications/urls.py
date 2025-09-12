from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.get_notifications, name='get_notifications'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('mark-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]