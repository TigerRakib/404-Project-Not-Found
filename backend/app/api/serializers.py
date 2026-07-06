from rest_framework import serializers
from .models import Task, AnnotationImage


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class AnnotationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationImage
        fields = '__all__'
