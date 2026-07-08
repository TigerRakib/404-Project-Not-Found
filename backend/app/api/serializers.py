from rest_framework import serializers
from .models import Task, AnnotationImage, PolygonAnnotation


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user',)


class AnnotationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationImage
        fields = '__all__'
        read_only_fields = ('user',)


class PolygonAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonAnnotation
        fields = '__all__'


class PolygonAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonAnnotation
        fields = '__all__'
