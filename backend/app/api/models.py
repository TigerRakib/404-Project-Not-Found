from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    """
    Represents an item within the user's Kanban workspace.
    Tasks are filtered strictly by their execution date.
    """
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ]
    
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done')
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        help_text="The main-character developer owner of this task node."
    )
    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='TODO')
    due_date = models.DateField(help_text="The targeted timeline boundary for calendar matching.")
    tags = models.JSONField(default=list, blank=True, help_text="Array string metadata elements.")

    class Meta:
        ordering = ['due_date', '-id']

    def __str__(self):
        return f"{self.title} | {self.status} ({self.priority})"