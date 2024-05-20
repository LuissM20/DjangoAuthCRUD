from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'home.html')

# Esta vista registra al usuario en la base de datos por medio de un formulario


def signup(request):

    # Pregunta si esta solicitando la vista o está enviando datos
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        # Valida si las contraseñas del formulario coinciden
        if request.POST['password1'] == request.POST['password2']:
            # Registra al usuario en la base de datos
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                print(user)
                user.save()
                login(request, user)
                return redirect('tasks')
            # Si el username ya se encuentra en la base de datos devuelve al usuario al formulario con un error
            except:
                return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Username Already exists'})
        # Si las contraseñas no coinciden devuelve al usuario de nuevo al formulario con un error
        return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Password Do not Match'})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {'form': TaskForm, 'error': 'Error al procesar la petición'})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'Username or password is incorrect'})
        else:
            login(request, user)
        return redirect('home')

@login_required
def task_detail(request, id):
    if request.method == 'GET':
        task= get_object_or_404(Task,pk=id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task= get_object_or_404(Task,pk=id, user=request.user)
            form = TaskForm(request.POST, instance=task)                    
            form.save()
            return redirect('tasks')
        except:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error':'Error updating task'})
@login_required            
def complete_task(request,id):
    task=get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST': 
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required    
def delete_task(request,id):
    task=get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST': 
        task.delete()
        return redirect('tasks')    


    



        
         