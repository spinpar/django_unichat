from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from posts.models import Post,Event
from posts.forms import PostForm, EventForm
from chat.models import Room

@login_required
def home(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'post':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('home')
        elif form_type == 'event':
            event_form = EventForm(request.POST, request.FILES)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.author = request.user
                event.save()
                return redirect('home')
    form = PostForm()
    event_form = EventForm()
    user_course_id = None
    if request.user.profile.course.exists():
        user_course_id = request.user.profile.course.first().id
    teacher_posts = Post.objects.filter(
        Q(author__profile__is_teacher=True) &
        (
            Q(author__profile__course__id=user_course_id) |
            Q(author__profile__course__isnull=True)
        )
    ).distinct().select_related(
        'author__profile'
    ).prefetch_related(
        'comments__author__profile',
        'comments__replies__author__profile'
    ).order_by('-created_at')
    following_ids = request.user.profile.following.values_list('id', flat=True)
    query_filter = Q(author__id__in=following_ids)
    if user_course_id:
        query_filter |= Q(author__profile__course__id=user_course_id)
    student_posts = Post.objects.filter(
        query_filter
    ).filter(
        ~Q(author__profile__is_teacher=True)
    ).distinct().select_related(
        'author__profile'
    ).prefetch_related(
        'comments__author__profile',
        'comments__replies__author__profile'
    ).order_by('-created_at')


    all_posts = list(teacher_posts) + list(student_posts)


    events = Event.objects.filter(author__profile__is_teacher=True).order_by('event_date', 'event_time')

    rooms = Room.objects.all()

    context = {
        'rooms': rooms,
        'posts': all_posts,
        'form': form,
        'events': events,
        'event_form': event_form,
    }
    return render(request, 'home.html', context)

@login_required
def editar_evento(request, pk):
    event = get_object_or_404(Event, pk=pk, author=request.user)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Evento "{event.title}" atualizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Houve um erro ao salvar as alterações. Verifique os campos.')
    else:
        form = EventForm(instance=event)
        
    context = {
        'form': form,
        'event': event,
        'is_editing': True
    }
    
    return render(request, 'event_edit.html', context)

@login_required
@require_http_methods(["POST"]) 
def apagar_evento(request, pk):
    event = get_object_or_404(Event, pk=pk, author=request.user) 
    
    event.delete()
    messages.warning(request, f'Evento "{event.title}" apagado permanentemente.')
    return redirect('home')