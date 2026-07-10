from django.conf import settings
from rest_framework import serializers
from .models import Task, AnnotationImage, PolygonAnnotation


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class AnnotationImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnnotationImage
        fields = ('id', 'user', 'image', 'image_url', 'uploaded_at')
        read_only_fields = ('user', 'uploaded_at', 'image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if not obj.image:
            return None
        if request is None:
            return obj.image.url
        return request.build_absolute_uri(obj.image.url)

    def validate_image(self, value):
        # Validate file size
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', None)
        if max_size and value.size > max_size:
            raise serializers.ValidationError(f'Image file too large (>{max_size} bytes).')

        # Validate content type (basic check)
        content_type = getattr(value, 'content_type', None)
        if content_type and not content_type.startswith('image/'):
            raise serializers.ValidationError('Uploaded file is not an image.')

        return value


class PolygonAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonAnnotation
        fields = '__all__'
