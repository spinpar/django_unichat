# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URL de cadastro
    path('register', views.register, name='register'),

    # URL para a página de atualização de perfil
    path('profile/update/', views.profile_update, name='profile_update'),

    # URL para o perfil do usuário (remova a outra linha idêntica)
    path('profile/<str:username>/', views.profile_view, name='profile'),
    
    # URL para seguir/deixar de seguir
    path('follow/<str:username>/', views.follow_user, name='follow_user'),

    # URL para ver seguidores
    path('profile/<str:username>/<str:list_type>/', views.get_follow_list, name='get_follow_list'),
]