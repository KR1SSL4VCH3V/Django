from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from task_manager.tasks.models import Task
from task_manager.tasks.views import HomeTaskView, DeleteTaskView

UserModel = get_user_model()


class TestTaskView(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserModel.objects.create_user(
            username='test_user', password='test_password'
        )
        self.token = Token.objects.create(user=self.user)
        self.view = HomeTaskView.as_view()

        self.url = '/api/home/'

    def test_get_task_authenticated(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user, token=self.token)

        response = self.view(request)

        self.assertEqual(response.status_code, 200)

    def test_list_tasks(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        data = {
            'title': 'test',
            'description': '',
            'priority': False,
            'created_date': '',
        }
        request = self.factory.post(self.url, data)
        force_authenticate(request, user=self.user, token=self.token)

        view_func = self.view
        response = view_func(request)

        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'test')

    def test_delete_task(self):
        task = Task.objects.create(title='test')
        url = f'/api/delete/{task.pk}/'
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = DeleteTaskView.as_view()(request, pk=task.pk)

        response = view

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=task.id).exists())
