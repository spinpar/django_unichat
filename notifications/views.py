from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST

@login_required
def get_notifications(request):
    """View para retornar as 10 notificações mais recentes e não lidas do usuário."""
    notifications = Notification.objects.filter(
        recipient=request.user, 
        is_read=False
    ).select_related(
        'actor__profile' # Otimiza a busca pelo autor e seu perfil
    ).order_by('-timestamp')[:10] # Limita a 10 resultados

    notifications_data = []
    for notification in notifications:
        target_url = '#'
        if notification.target:
            if notification.content_type.model == 'post':
                target_url = f'/posts/{notification.target.id}/' 
            elif notification.content_type.model == 'user':
                target_url = f'/profile/{notification.target.username}/'
            elif notification.content_type.model == 'comment':
                if hasattr(notification.target, 'post'):
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
@require_POST
def mark_all_read(request):
    """View para marcar todas as notificações de um usuário como lidas."""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def mark_as_read(request, notification_id):
    """View para marcar uma notificação específica como lida."""
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notificação não encontrada.'}, status=404)