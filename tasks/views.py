from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from .models import STATE_CHOICES, PRIORITY_CHOICES


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')  # Redirige a la página de inicio después de iniciar sesión
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    form = AuthenticationForm()  # Crear una nueva instancia del formulario de inicio de sesión
    return render(request, 'tasks/login.html', {'form': form})

@login_required
def task_list(request):
    query = request.GET.get('q')  # Captura el término de búsqueda
    state_filter = request.GET.get('state')  # Captura el filtro de estado
    priority_filter = request.GET.get('priority')  # Captura el filtro de prioridad
    due_date = request.GET.get('due_date')  # Captura el filtro de fecha

    # Filtrar por título, estado, prioridad o fecha según lo que se haya ingresado en la barra de búsqueda o filtros
    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(title__icontains=query)  # Búsqueda por título

    if state_filter:
        tasks = tasks.filter(state=state_filter)  # Filtrar por estado

    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)  # Filtrar por prioridad

    if due_date:
        tasks = tasks.filter(due_date__date=due_date)  # Filtrar por fecha exacta

    # Paginación: mostrar 10 tareas por página
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Si el número de página no es un entero, muestra la primera página
        page_obj = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera de rango, muestra la última página
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'tasks/task_list.html', {
        'page_obj': page_obj,
        'STATE_CHOICES': STATE_CHOICES,
        'PRIORITY_CHOICES': PRIORITY_CHOICES,  # Pasar las opciones al contexto
    })



@login_required
def task_create_update(request, task_id=None):
    if task_id:
        task = get_object_or_404(Task, id=task_id)  # Obtener la tarea si existe (edición)
    else:
        task = None  # Si no hay task_id, significa que estamos creando una nueva tarea

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.created_by = request.user  # Asignar el usuario que creó la tarea
            new_task.save()
            return redirect('task_list')  # Redirigir a la lista de tareas después de guardar
    else:
        form = TaskForm(instance=task)  # Pre-llenar el formulario con los datos de la tarea (en caso de edición)

    return render(request, 'tasks/task_form.html', {'form': form, 'task': task})


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'La tarea fue eliminada exitosamente.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})



