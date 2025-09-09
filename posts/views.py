# posts/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Reply, Vote
from .forms import CommentForm, ReplyForm

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
            return redirect('home')
    return redirect('home')

@login_required
def vote_post(request, post_id, vote_type):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    existing_vote = Vote.objects.filter(user=user, post=post).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            existing_vote.delete()
        else:
            existing_vote.vote_type = vote_type
            existing_vote.save()
    else:
        Vote.objects.create(user=user, post=post, vote_type=vote_type)

    return redirect('home')