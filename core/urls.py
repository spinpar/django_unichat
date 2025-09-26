from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('evento/editar/<int:pk>/', views.editar_evento, name='editar_evento'),

    path('evento/apagar/<int:pk>/', views.apagar_evento, name='apagar_evento')
]