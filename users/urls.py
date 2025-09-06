from django.urls import path
from . import views

urlpatterns = [
     # URL de cadastro
    path('', views.register, name='register'),

    # URL de Perfil
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
]