# notifications/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def get_notifications(request):
    """View para retornar as notificações não lidas do usuário logado."""
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-timestamp')
    
    notifications_data = []
    for notification in notifications:
        # Pega a URL do objeto relacionado (Post, User, Comment, etc.)
        # Exemplo: se for um Post, pega a URL do Post
        # Você precisará ajustar as URLs de acordo com sua lógica
        target_url = '#'
        if notification.target:
            if notification.content_type.model == 'post':
                # Supondo que você tenha uma URL para ver posts individuais
                target_url = f'/posts/{notification.target.id}/' 
            elif notification.content_type.model == 'user':
                target_url = f'/profile/{notification.target.username}/'
            elif notification.content_type.model == 'comment':
                # Lógica para redirecionar ao post do comentário
                target_url = f'/posts/{notification.target.post.id}/'
        
        notifications_data.append({
            'id': notification.id,
            'actor_username': notification.actor.username,
            'actor_avatar_url': notification.actor.profile.avatar.url if notification.actor.profile.avatar else '/static/img/default_profile.png',
            'verb': notification.verb,
            'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'target_url': target_url
        })

    return JsonResponse({'notifications': notifications_data})


@login_required
def mark_all_read(request):
    """View para marcar todas as notificações de um usuário como lidas."""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})