from django.urls import path
from . import views  # Importar las vistas desde views.py

urlpatterns = [
    path('', views.task_list, name='task_list'),  # Ruta para la página principal (que puede ser una lista de tareas)
    path('login/', views.login_view, name='login'),  # Ruta para el inicio de sesión
    path('logout/', views.logout_view, name='logout'),  # Ruta para cerrar sesión
    path('tasks/', views.task_list, name='task_list'),  # Ruta para la lista de tareas
    path('tasks/create/', views.task_create_update, name='task_create'),  # Ruta para crear tarea
    path('tasks/<int:task_id>/edit/', views.task_create_update, name='task_update'),  # Ruta para editar tarea
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),  # Ruta para eliminar tarea
]

