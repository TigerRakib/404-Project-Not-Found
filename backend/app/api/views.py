from rest_framework import viewsets, permissions

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
	"""Simple Task CRUD API."""
	queryset = Task.objects.all().order_by('-id')
	serializer_class = TaskSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

