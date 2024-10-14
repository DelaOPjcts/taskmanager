from django.db import models
from django.contrib.auth.models import User

# opciones para el estado
STATE_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('on_hold', 'On Hold'),
    ('completed', 'Completed'),
    ('canceled', 'Canceled'),
    ('reviewed', 'Reviewed'),
    ('failed', 'Failed'),
]

# opciones para la prioridad
PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
]


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)  # Cambia Usuario a User
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)  # Cambia Usuario a User
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)

