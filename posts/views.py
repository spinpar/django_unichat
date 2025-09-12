# posts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Reply, Vote
from .forms import CommentForm, ReplyForm
from django.http import JsonResponse, HttpResponseRedirect
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

# Views para adicionar comentários e respostas
@login_required
def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            
            if request.user != post.author:
                post_content_type = ContentType.objects.get_for_model(Post)
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='comentou em seu post',
                    content_type=post_content_type,
                    object_id=post.id
                )
                return redirect('home')

    return redirect('home')

@login_required
def add_reply_to_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.comment = comment
            reply.save()

            if request.user != comment.author:
                comment_content_type = ContentType.objects.get_for_model(Comment)
                Notification.objects.create(
                    recipient=comment.author,
                    actor=request.user,
                    verb='respondeu ao seu comentário',
                    content_type=comment_content_type,
                    object_id=comment.id
                )
            return redirect('home')
    return redirect('home')

@login_required
def vote_post(request, post_id, vote_type):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if vote_type not in ['like', 'dislike']:
        return JsonResponse({'error': 'Tipo de voto inválido'}, status=400)

    existing_vote = Vote.objects.filter(user=user, post=post).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            existing_vote.delete()
        else:
            existing_vote.vote_type = vote_type
            existing_vote.save()
            if vote_type == 'like' and post.author != user:
                post_content_type = ContentType.objects.get_for_model(Post)
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb='curtiu seu post',
                    content_type=post_content_type,
                    object_id=post.id
                )
    else:
        Vote.objects.create(user=user, post=post, vote_type=vote_type)
        if vote_type == 'like' and post.author != user:
            post_content_type = ContentType.objects.get_for_model(Post)
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='curtiu seu post',
                content_type=post_content_type,
                object_id=post.id
            )

    likes_count = post.likes_count
    dislikes_count = post.dislikes_count

    return JsonResponse({
        'likes_count': likes_count,
        'dislikes_count': dislikes_count
    })

@login_required
def vote_comment(request, comment_id, vote_type):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if vote_type not in ['like', 'dislike']:
        return JsonResponse({'error': 'Tipo de voto inválido'}, status=400)

    existing_vote = Vote.objects.filter(user=user, comment=comment).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            existing_vote.delete()
        else:
            existing_vote.vote_type = vote_type
            existing_vote.save()
    else:
        Vote.objects.create(user=user, comment=comment, vote_type=vote_type)

    likes_count = comment.likes_count
    dislikes_count = comment.dislikes_count

    return JsonResponse({
        'likes_count': likes_count,
        'dislikes_count': dislikes_count
    })

@login_required
def vote_reply(request, reply_id, vote_type):
    reply = get_object_or_404(Reply, id=reply_id)
    user = request.user

    if vote_type not in ['like', 'dislike']:
        return JsonResponse({'error': 'Tipo de voto inválido'}, status=400)

    existing_vote = Vote.objects.filter(user=user, reply=reply).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            existing_vote.delete()
        else:
            existing_vote.vote_type = vote_type
            existing_vote.save()
    else:
        Vote.objects.create(user=user, reply=reply, vote_type=vote_type)
        
    likes_count = reply.likes_count
    dislikes_count = reply.dislikes_count

    return JsonResponse({
        'likes_count': likes_count,
        'dislikes_count': dislikes_count
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)