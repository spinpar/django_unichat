from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.user_search, name='user_search'),
]
