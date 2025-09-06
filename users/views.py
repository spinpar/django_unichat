# users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile

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

@login_required
def profile(request):
    """View para exibir as informações do perfil do usuário logado."""
    age = None
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)
    
    if user_profile.date_of_birth:
        today = date.today()
        birth_date = user_profile.date_of_birth
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    context = {
        'user': request.user,
        'profile': user_profile,
        'age': age,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_update(request):
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('profile')
        else:
            print("Erros no formulário de usuário:", u_form.errors)
            print("Erros no formulário de perfil:", p_form.errors)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile_update.html', context)

def user_profile(request, username):
    """View para exibir as informações de perfil de qualquer usuário."""
    # Tenta obter o usuário pelo nome de usuário; se não encontrar, retorna 404
    user = get_object_or_404(User, username=username)
    
    # Adicione a mesma lógica para verificar o perfil e calcular a idade
    age = None
    try:
        profile_data = user.profile
        if profile_data.date_of_birth:
            today = date.today()
            age = today.year - profile_data.date_of_birth.year - ((today.month, today.day) < (profile_data.date_of_birth.month, profile_data.date_of_birth.day))
    except Profile.DoesNotExist:
        profile_data = None  # Define como None se o perfil não existir
    
    context = {
        'user_data': user,
        'profile_data': profile_data,
        'age': age,
    }
    return render(request, 'users/user_profile.html', context)