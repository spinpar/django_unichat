from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from users.models import Profile, Course 

def user_search(request):
    query = request.GET.get('q', '')
    if query:
        search_terms = query.split()
        query_set = Q()

        for term in search_terms:
            query_set |= (
                Q(username__icontains=term) |
                Q(first_name__icontains=term) |
                Q(last_name__icontains=term) |
                Q(profile__course__name__icontains=term)
            )
        
        results = User.objects.filter(query_set).distinct().select_related('profile')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user_list = []
            for user in results:
                avatar_url = user.profile.avatar.url if user.profile.avatar else '/static/img/default_profile.png'
                user_list.append({
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'avatar_url': avatar_url,
                })
            return JsonResponse({'users': user_list})

    context = {
        'query': query,
        'results': results, 
    }
    return render(request, 'searchcontent/user_search_results.html', context)