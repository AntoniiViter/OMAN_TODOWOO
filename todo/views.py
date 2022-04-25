from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method=='GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})

def loginuser(request):
    if request.method=='GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': "Username and password didn't match"})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method=='GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.todocreator = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in. Try again'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(todocreator=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required
def viewtodo(request, todo_id):
    viewtodo = get_object_or_404(Todo, pk=todo_id, todocreator=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=viewtodo)
        return render(request, 'todo/viewtodo.html', {'viewtodo': viewtodo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=viewtodo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in. Try again'})

def completetodo(request, todo_id):
    completetodos = get_object_or_404(Todo, pk=todo_id, todocreator=request.user)
    if request.method == 'POST':
        completetodos.datecompleted = timezone.now()
        completetodos.save()
        return redirect('currenttodos')

def deletetodo(request, todo_id):
    deletedtodos = get_object_or_404(Todo, pk=todo_id, todocreator=request.user)
    if request.method == 'POST':
        deletedtodos.delete()
        return redirect('currenttodos')

def deletetodo_completed(request, todo_id):
    deletedtodos = get_object_or_404(Todo, pk=todo_id, todocreator=request.user)
    if request.method == 'POST':
        deletedtodos.delete()
        return redirect('completedtodos')

@login_required
def completedtodos(request):
    completetodos = Todo.objects.filter(todocreator=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': completetodos})