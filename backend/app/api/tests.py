import io
import json
import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from .models import Task, AnnotationImage, PolygonAnnotation


class TaskEndpointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)
        self.list_url = reverse('task-list')

    def test_list_tasks(self):
        Task.objects.create(user=self.user, title='Task 1', due_date='2026-12-31')
        Task.objects.create(user=self.user, title='Task 2', due_date='2026-12-31')

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task_authenticated(self):
        payload = {
            'user': self.user.id,
            'title': 'New Task',
            'priority': 'HIGH',
            'status': 'TODO',
            'due_date': '2026-12-31',
            'tags': ['api', 'test'],
        }

        response = self.auth_client.post(self.list_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(response.data['title'], 'New Task')

    def test_retrieve_task(self):
        task = Task.objects.create(user=self.user, title='Retrieve Task', due_date='2026-12-31')
        url = reverse('task-detail', args=[task.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)

    def test_update_task_authenticated(self):
        task = Task.objects.create(user=self.user, title='Old Title', due_date='2026-12-31')
        url = reverse('task-detail', args=[task.id])

        response = self.auth_client.patch(url, {'title': 'New Title'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'New Title')

    def test_delete_task_authenticated(self):
        task = Task.objects.create(user=self.user, title='Delete Task', due_date='2026-12-31')
        url = reverse('task-detail', args=[task.id])

        response = self.auth_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())


class AnnotationImageEndpointTests(TestCase):
    def setUp(self):
        self.temp_media_root = tempfile.mkdtemp()
        self.override_settings = override_settings(MEDIA_ROOT=self.temp_media_root)
        self.override_settings.enable()
        self.user = User.objects.create_user(username='imageuser', password='password')
        self.client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)
        self.list_url = reverse('annotationimage-list')

    def tearDown(self):
        self.override_settings.disable()
        shutil.rmtree(self.temp_media_root, ignore_errors=True)

    def _create_image_file(self):
        image_io = io.BytesIO()
        image = Image.new('RGB', (10, 10), color='white')
        image.save(image_io, format='PNG')
        image_io.seek(0)
        return SimpleUploadedFile('test.png', image_io.read(), content_type='image/png')

    def test_list_annotation_images(self):
        AnnotationImage.objects.create(user=self.user, image=self._create_image_file())

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_annotation_image_authenticated(self):
        payload = {'user': self.user.id, 'image': self._create_image_file()}

        response = self.auth_client.post(self.list_url, payload, format='multipart')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f'Unexpected response: {response.status_code} {response.data}'
        )
        self.assertEqual(AnnotationImage.objects.count(), 1)
        self.assertIn('image', response.data)

    def test_retrieve_annotation_image(self):
        image = AnnotationImage.objects.create(user=self.user, image=self._create_image_file())
        url = reverse('annotationimage-detail', args=[image.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], image.id)

    def test_delete_annotation_image_authenticated(self):
        image = AnnotationImage.objects.create(user=self.user, image=self._create_image_file())
        url = reverse('annotationimage-detail', args=[image.id])

        response = self.auth_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AnnotationImage.objects.filter(id=image.id).exists())


class PolygonAnnotationEndpointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='polygonuser', password='password')
        self.client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)
        self.image = AnnotationImage.objects.create(
            user=self.user,
            image=SimpleUploadedFile(
                'test.png',
                b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0bIDAT\x08\xd7c\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\x8d\x83\x00\x00\x00\x00IEND\xaeB`\x82',
                content_type='image/png'
            ),
        )
        self.list_url = reverse('polygonannotation-list')

    def test_list_polygon_annotations(self):
        PolygonAnnotation.objects.create(image=self.image, points=[[0.1, 0.1], [0.2, 0.2]], label='Test')

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_polygon_annotation_authenticated(self):
        payload = {
            'image': self.image.id,
            'points': [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
            'label': 'Polygon Test',
        }

        response = self.auth_client.post(self.list_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PolygonAnnotation.objects.count(), 1)
        self.assertEqual(response.data['label'], 'Polygon Test')

    def test_retrieve_polygon_annotation(self):
        polygon = PolygonAnnotation.objects.create(image=self.image, points=[[0.1, 0.1], [0.2, 0.2]], label='Detail')
        url = reverse('polygonannotation-detail', args=[polygon.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], polygon.label)

    def test_update_polygon_annotation_authenticated(self):
        polygon = PolygonAnnotation.objects.create(image=self.image, points=[[0.1, 0.1]], label='Old Label')
        url = reverse('polygonannotation-detail', args=[polygon.id])

        response = self.auth_client.patch(url, {'label': 'New Label'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        polygon.refresh_from_db()
        self.assertEqual(polygon.label, 'New Label')

    def test_delete_polygon_annotation_authenticated(self):
        polygon = PolygonAnnotation.objects.create(image=self.image, points=[[0.1, 0.1]], label='Delete')
        url = reverse('polygonannotation-detail', args=[polygon.id])

        response = self.auth_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PolygonAnnotation.objects.filter(id=polygon.id).exists())
