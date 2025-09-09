from django.urls import path
from . import views

app_name = 'posts' # Adicione esta linha

urlpatterns = [
    path('post/<int:post_id>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:comment_id>/reply/', views.add_reply_to_comment, name='add_reply_to_comment'),
    path('post/<int:post_id>/vote/<str:vote_type>/', views.vote_post, name='vote_post'),
]