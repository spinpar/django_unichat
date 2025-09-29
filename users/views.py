# users/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from django.db.models import F, Count, Q
from posts.models import Post, Vote, Event
from posts.forms import PostForm, EventForm
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso para {username}! Você já pode fazer login.')
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def profile_view(request, username=None):
    if username is None:
        return redirect('profile', username=request.user.username)

    target_user = get_object_or_404(User, username=username)

    try:
        target_profile = target_user.profile
    except Profile.DoesNotExist:
        target_profile = Profile.objects.create(user=target_user)
    
    is_following = False
    if request.user.is_authenticated:
        if request.user != target_user:
            is_following = request.user.profile.following.filter(id=target_user.id).exists()
    
    followers_count = target_user.followers.count() 
    following_count = target_profile.following.count() 
    
    age = None
    if target_profile.date_of_birth:
        today = date.today()
        birth_date = target_profile.date_of_birth
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    posts = Post.objects.filter(
        author=target_user
    ).select_related(
        'author__profile'
    ).prefetch_related(
        'comments__author__profile',
        'comments__replies__author__profile'
    ).order_by('-created_at')

    context = {
        'target_user': target_user,
        'target_profile': target_profile,
        'is_following': is_following,
        'age': age,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts': posts,
    }
    
    return render(request, 'users/profile.html', context)

@login_required
def profile_update(request):
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    is_teacher_user = user_profile.is_teacher

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

        if 'date_of_birth' in request.POST and request.POST['date_of_birth']:
            try:
                user_profile.date_of_birth = datetime.strptime(request.POST['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Formato de data inválido. Por favor, use AAAA-MM-DD.')
                return redirect('profile_update')
        else:
            pass 

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            user_profile.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('profile', username=request.user.username )
        else:
            messages.error(request, 'O formulário tem erros. Por favor, corrija-os.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile, is_teacher=is_teacher_user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile_update.html', context)

def user_profile(request, username):
    """View para exibir as informações de perfil de qualquer usuário."""
    user = get_object_or_404(User, username=username)
    
    age = None
    try:
        profile_data = user.profile
        if profile_data.date_of_birth:
            today = date.today()
            age = today.year - profile_data.date_of_birth.year - ((today.month, today.day) < (profile_data.date_of_birth.month, profile_data.date_of_birth.day))
    except Profile.DoesNotExist:
        profile_data = None
    
    context = {
        'user_data': user,
        'profile_data': profile_data,
        'age': age,
    }
    return render(request, 'users/user_profile.html', context)

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    user_profile = request.user.profile

    if user_profile.following.filter(id=target_user.id).exists():
        user_profile.following.remove(target_user)
    else:
        user_profile.following.add(target_user)

        if request.user != target_user:
            user_content_type = ContentType.objects.get_for_model(User)
            Notification.objects.create(
                recipient=target_user,
                actor=request.user,
                verb='começou a te seguir',
                content_type=user_content_type,
                object_id=target_user.id
            )

    return redirect('profile', username=username)

@login_required
def get_follow_list(request, username, list_type):
    target_user = get_object_or_404(User, username=username)
    
    user_list = []
    
    if list_type == 'followers':
        profiles = target_user.followers.select_related('user').all()
        user_list = [
            {
                'username': p.user.username,
                'first_name': p.user.first_name,
                'last_name': p.user.last_name,
                'avatar_url': p.avatar.url if p.avatar else '/static/img/default_profile.png'
            } 
            for p in profiles
        ]
    elif list_type == 'following':
        following_users = target_user.profile.following.all()
        user_list = [
            {
                'username': u.username,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'avatar_url': u.profile.avatar.url if hasattr(u, 'profile') and u.profile.avatar else '/static/img/default_profile.png'
            }
            for u in following_users
        ]

    return JsonResponse({'users': user_list})

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
            event_form = EventForm(request.POST)
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


    context = {
        'posts': all_posts,
        'form': form,
        'events': events,
        'event_form': event_form,
    }
    return render(request, 'home.html', context)

def login_view(request):
    error = False  # Flag para controlar erro de login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Loga o usuário
            return redirect('home')  # Redireciona para home
        else:
            error = True  # Usuário ou senha incorretos

    return render(request, 'users/login.html', {'error': error})
