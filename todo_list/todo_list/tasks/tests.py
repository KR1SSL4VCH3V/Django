from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from task_manager.tasks.views import HomeTaskView

UserModel = get_user_model()


class TestTaskView(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = '/api/home/'
        self.view = HomeTaskView.as_view()
        self.user = UserModel.objects.create_user(
            username='test_user', password='test_password'
        )
        self.token = Token.objects.create(user=self.user)

    def test_get_task_authenticated(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user, token=self.token)

        response = self.view(request)

        self.assertEqual(response.status_code, 200)
