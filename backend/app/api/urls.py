from django.urls import include, path
from rest_framework import routers
from .views import (
    TaskViewSet,
    AnnotationImageViewSet,
    PolygonAnnotationViewSet,
    signup_view,
    login_view,
    logout_view,
    current_user,
)

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'annotation-images', AnnotationImageViewSet, basename='annotationimage')
router.register(r'polygon-annotations', PolygonAnnotationViewSet, basename='polygonannotation')

urlpatterns = [
    path('auth/signup/', signup_view, name='signup'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/user/', current_user, name='current_user'),
    path('', include(router.urls)),
]
