import json

from django.test import RequestFactory, TestCase

from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.tasks.views import HomeTaskView, EditTaskView, DeleteTaskView

UserModel = get_user_model()


class TaskIntegrationTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='test_user', password='test_password')
        self.factory = RequestFactory()

    def test_home_task_view(self):
        request = self.factory.get('/home/')
        force_authenticate(request, user=self.user)
        response = HomeTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task_view(self):
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': False,
            'due_date': '2024-03-23',
        }
        request = self.factory.post('/home/', data=json.dumps(task_data), content_type='application/json')
        force_authenticate(request, user=self.user)
        response = HomeTaskView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_edit_task_view(self):
        task = Task.objects.create(title='Existing Task')
        edit_data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': True,
            'due_date': '2024-03-23',
        }
        request = self.factory.put(f'/edit/{task.pk}/', data=json.dumps(edit_data), content_type='application/json')
        force_authenticate(request, user=self.user)
        response = EditTaskView.as_view()(request, pk=task.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')

    def test_delete_task_view(self):
        task = Task.objects.create(title='Task to Delete')
        request = self.factory.delete(f'/delete/{task.pk}/')
        force_authenticate(request, user=self.user)
        response = DeleteTaskView.as_view()(request, pk=task.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=task.id).exists())
