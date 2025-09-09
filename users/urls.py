from django.urls import path
from . import views

urlpatterns = [
    # URL de cadastro
    path('', views.register, name='register'),

    # URL para a página de atualização de perfil
    path('profile/update/', views.profile_update, name='profile_update'),

    # URL para o perfil do usuário logado E o de outros usuários
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('profile/', views.profile_view, name='profile'),
    
    # URL para seguir/deixar de seguir
    path('follow/<str:username>/', views.follow_user, name='follow_user'),

    # URL para ver seguidores
    path('profile/<str:username>/<str:list_type>/', views.get_follow_list, name='get_follow_list'),
]