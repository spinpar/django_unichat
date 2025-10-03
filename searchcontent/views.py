from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from users.models import Profile, Course 
from posts.models import Post

def user_search(request):
    query = request.GET.get('q', '')
    if query:
        search_terms = query.split()
        user_query_set = Q()
        for term in search_terms:
            user_query_set |= (
                Q(username__icontains=term) |
                Q(first_name__icontains=term) |
                Q(last_name__icontains=term) |
                Q(profile__course__name__icontains=term)
            )
        post_query_set = Q()
        for term in search_terms:
            post_query_set |= (
                Q(content__icontains=term) |
                Q(author__first_name__icontains=term) |
                Q(author__last_name__icontains=term) |
                Q(author__username__icontains=term)
            )
        user_results = User.objects.filter(user_query_set).distinct().select_related('profile')
        post_results = Post.objects.filter(post_query_set).distinct().select_related('author__profile')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    
            user_list = []
            for user in user_results:
                avatar_url = user.profile.avatar.url if user.profile.avatar else '/static/img/default_profile.png'
                user_list.append({
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'avatar_url': avatar_url,
                })
            
            post_list = []
            for post in post_results:
                post_list.append({
                    'id': post.id,
                    'content': post.content[:50] + '...',
                    'author_username': post.author.username,
                    'author_avatar': post.author.profile.avatar.url if post.author.profile.avatar else '/static/img/default_profile.png'
                })

            return JsonResponse({'users': user_list, 'posts': post_list})

    context = {
        'query': query,
        'user_results': user_results,
        'post_results': post_results,
    }
    return render(request, 'searchcontent/user_search_results.html', context)