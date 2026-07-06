from django.urls import include, path
from rest_framework import routers
from .views import TaskViewSet, AnnotationImageViewSet, PolygonAnnotationViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'annotation-images', AnnotationImageViewSet, basename='annotationimage')
router.register(r'polygon-annotations', PolygonAnnotationViewSet, basename='polygonannotation')

urlpatterns = [
    path('', include(router.urls)),
]
