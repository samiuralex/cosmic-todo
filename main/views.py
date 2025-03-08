from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse
from .models import Todo
from .forms import TodoForm, CustomUserCreationForm, CustomAuthenticationForm

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    total_users = User.objects.count()
    total_todos = Todo.objects.count()
    completed_todos = Todo.objects.filter(completed=True).count()
    completion_rate = (completed_todos / total_todos * 100) if total_todos > 0 else 0
    
    context = {
        'total_users': total_users,
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'completion_rate': round(completion_rate, 1)
    }
    return render(request, 'main/landing.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome aboard, Space Explorer! Your cosmic journey begins now.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'main/register.html', {
        'form': form,
        'title': 'Join the Mission'
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, Commander {user.username}!')
                next_url = request.GET.get('next')
                return redirect(next_url if next_url else 'home')
        else:
            messages.error(request, 'Mission control denied access. Please check your credentials.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'main/login.html', {
        'form': form,
        'title': 'Mission Control Access'
    })

def logout_view(request):
    logout(request)
    messages.info(request, 'You have safely returned to Earth. Come back soon!')
    return redirect('landing_page')

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Mission launched successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Mission launch failed. Please check your mission parameters.')
    else:
        form = TodoForm()
    
    user_todos = Todo.objects.filter(user=request.user)
    todos = user_todos.filter(completed=False).order_by('-priority', 'due_date', '-created_date')
    completed_todos = user_todos.filter(completed=True).order_by('-completed_date')[:5]
    
    # User statistics
    total_missions = user_todos.count()
    completed_missions = user_todos.filter(completed=True).count()
    completion_rate = (completed_missions / total_missions * 100) if total_missions > 0 else 0
    
    context = {
        'form': form,
        'todos': todos,
        'completed_todos': completed_todos,
        'total_missions': total_missions,
        'completed_missions': completed_missions,
        'completion_rate': round(completion_rate, 1),
        'title': 'Mission Control'
    }
    return render(request, 'main/home.html', context)

@login_required(login_url='login')
def complete_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.completed = True
        todo.save()
        messages.success(request, 'Mission accomplished! Well done, Commander!')
    return redirect('home')

@login_required(login_url='login')
def delete_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.delete()
        messages.success(request, 'Mission aborted successfully.')
    return redirect('home')
