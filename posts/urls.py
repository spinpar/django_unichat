# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('post/<int:post_id>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:comment_id>/reply/', views.add_reply_to_comment, name='add_reply_to_comment'),
    path('post/<int:post_id>/vote/<str:vote_type>/', views.vote_post, name='vote_post'),
    path('comment/<int:comment_id>/vote/<str:vote_type>/', views.vote_comment, name='vote_comment'),
    path('reply/<int:reply_id>/vote/<str:vote_type>/', views.vote_reply, name='vote_reply'),
    path('<int:post_id>/', views.post_detail, name='post_detail'), 

]