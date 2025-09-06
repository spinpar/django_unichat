
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

def user_search(request):
	query = request.GET.get('q', '')
	results = []
	if query:
		results = User.objects.filter(
			Q(username__icontains=query) |
			Q(first_name__icontains=query) |
			Q(last_name__icontains=query)
		)
	context = {
		'query': query,
		'results': results,
	}
	return render(request, 'searchcontent/user_search_results.html', context)
