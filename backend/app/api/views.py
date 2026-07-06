from rest_framework import viewsets, permissions

from .models import Task, AnnotationImage
from .serializers import TaskSerializer, AnnotationImageSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Simple Task CRUD API."""
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnnotationImageViewSet(viewsets.ModelViewSet):
    """CRUD API for uploaded annotation images."""
    queryset = AnnotationImage.objects.all().order_by('-id')
    serializer_class = AnnotationImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

