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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # position is optional and can be used for ordering in a Kanban/drag-drop UI
    position = models.IntegerField(null=True, blank=True, db_index=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='TODO')
    due_date = models.DateField(help_text="The targeted timeline boundary for calendar matching.")
    tags = models.JSONField(default=list, blank=True, help_text="Array string metadata elements.")

    class Meta:
        # Prefer explicit position ordering when present, then newest first
        ordering = ['position', '-created_at']

    def __str__(self):
        return f"{self.title} | {self.status} ({self.priority})"
    
class AnnotationImage(models.Model):
    """
    Stores an image asset uploaded to the backend server, 
    intended to host vector structural markings.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(
        upload_to='annotations/',
        help_text="Binary image framework target payload."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image #{self.id} uploaded by {self.user.username}"
    
class PolygonAnnotation(models.Model):
    """
    Represents a specific closed multi-point polygon shape traced 
    manually over an explicit parent target image block.
    """
    image = models.ForeignKey(
        AnnotationImage, 
        on_delete=models.CASCADE, 
        related_name='polygons',
        help_text="The parent background digital image surface."
    )
    points = models.JSONField(
        help_text="Normalized relative coordinates list schema: [[x1, y1], [x2, y2], ...]"
    )
    label = models.CharField(max_length=100, blank=True, help_text="Optional semantic class label identifier.")

    def __str__(self):
        return f"Polygon {self.id} on Image #{self.image.id}"