from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Task, AnnotationImage, PolygonAnnotation
from .serializers import (
    TaskSerializer,
    AnnotationImageSerializer,
    PolygonAnnotationSerializer,
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response(
            {'detail': 'Username, email, and password are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username__iexact=username).exists():
        return Response(
            {'detail': 'Username already exists.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email__iexact=email).exists():
        return Response(
            {'detail': 'Email already exists.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username_or_email = request.data.get('email') or request.data.get('username')
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response(
            {'detail': 'Email/username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=username_or_email, password=password)
    if user is None:
        try:
            user_obj = User.objects.get(email__iexact=username_or_email)
        except User.DoesNotExist:
            user_obj = None
        if user_obj is not None:
            user = authenticate(
                request, username=user_obj.username, password=password
            )

    if user is None:
        return Response(
            {'detail': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
        }
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    if request.auth is not None:
        request.auth.delete()
    return Response({'detail': 'Logged out.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user = request.user
    return Response(
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
    )


class TaskViewSet(viewsets.ModelViewSet):
    """Simple Task CRUD API."""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-id')

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return get_object_or_404(queryset, pk=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnnotationImageViewSet(viewsets.ModelViewSet):
    """CRUD API for uploaded annotation images."""
    serializer_class = AnnotationImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnnotationImage.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PolygonAnnotationViewSet(viewsets.ModelViewSet):
    """CRUD API for polygon annotations."""
    serializer_class = PolygonAnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PolygonAnnotation.objects.filter(
            image__user=self.request.user
        ).order_by('-id')

    def perform_create(self, serializer):
        image = serializer.validated_data.get('image')
        if image.user != self.request.user:
            raise permissions.PermissionDenied(
                'Cannot annotate images owned by another user.'
            )
        serializer.save()

