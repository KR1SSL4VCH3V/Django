from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from task_manager.accounts.views import RegisterView, LogInView

UserModel = get_user_model()


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = '/register/'

    def test_register_view_success(self):
        data = {
            'username': 'John',
            'email': 'john@cena.com',
            'password1': 'Password12!',
            'password2': 'Password12!'
        }

        request = self.factory.post(self.url, data, format='json')
        view = RegisterView.as_view()

        response = view(request)
        

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('serializer', response.data)

    def test_register_view_unsuccessful(self):
        data = {
            'username': 'J',
            'email': 'johncena.com',
            'password1': 'password12',
            'password2': 'password12'
        }

        request = self.factory.post('/register/', data, format='json')
        view = RegisterView.as_view()

        response = view(request)
       

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LogInViewTest(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='test', password='test')
        self.factory = APIRequestFactory()
        self.view = LogInView.as_view()
        self.url = '/login/'
        self.data = {'username': 'test', 'password': 'test'}

    def test_login_success(self):
        request = self.factory.post(self.url, self.data)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'token')
