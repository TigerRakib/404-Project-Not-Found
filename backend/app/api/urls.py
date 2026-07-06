from django.urls import include, path
from rest_framework import routers
from .views import TaskViewSet, AnnotationImageViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'annotation-images', AnnotationImageViewSet, basename='annotationimage')

urlpatterns = [
    path('', include(router.urls)),
]
