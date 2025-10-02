# unichat/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # URLs de autenticação do Django, como login, logout, etc.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # URL principal que aponta para a home page
    path('', include('core.urls')),
    
    # URLs do seu app 'users'
    path('', include('users.urls')),

    # URLs do seu app 'searchcontent'
    path('search/', include('searchcontent.urls')),

    # URLs do seu app 'posts'
    path('posts/', include('posts.urls', namespace='posts')),
    
    # URL do painel de administração
    path('admin/', admin.site.urls),

    # URL do painel de notificação
    path('notifications/', include('notifications.urls')),

    # URL do chat
    path('ws/chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)