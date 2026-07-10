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
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
