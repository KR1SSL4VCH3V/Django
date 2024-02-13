from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from task_manager.accounts.views import RegisterView, LogInView, EditAccountView, DeleteAccountView

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
        print(response.data)

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

    def test_login_valid_credentials(self):
        request = self.factory.post(self.url, self.data)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'token')

    def test_login_invalid_credentials(self):
        invalid_data = {
            'username': 'test',
            'password': 'wrong_password',
        }

        request = self.factory.post(self.url, invalid_data)
        response = self.view(request)

        self.assertEqual(response.status_code, 400)
        # self.assertContains(response, 'Invalid username or password.')

    def test_login_missing_fields(self):
        missing_data = {
            'username': '',
            'password': ''
        }
        request = self.factory.post(self.url, missing_data)

        response = self.view(request)

        self.assertEqual(response.status_code, 400)


class TestEditAccountView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = EditAccountView.as_view()
        self.user = UserModel.objects.create_user(
            username='test_user',
            password='test_password',
        )
        self.token = Token.objects.create(user=self.user)
        self.url = f'/api/accounts/edit/{self.user.pk}/'

    def test_edit_account_valid(self):
        valid_data = {
            'username': 'new_username',
            'email': 'new_email@example.com',
            'new_password1': 'Test123!',
            'new_password2': 'Test123!',
        }

        request = self.factory.put(self.url, valid_data, 'json')
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk=self.user.pk)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Account updated successfully!')

    def test_edit_account_invalid(self):
        invalid_data = {
            'username': 'username',
            'email': 'email@example.com',
            'new_password1': 'test123!',
            'new_password2': 'test123!',
        }

        request = self.factory.put(self.url, invalid_data, 'json')
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk=self.user.pk)

        self.assertEqual(response.status_code, 400)

    def test_edit_account_permission_denied(self):
        other_user = UserModel.objects.create_user(username='other_user',
                                                   email='other@example.com',
                                                   password='password')
        url = f'/edit-account/{other_user.pk}/'
        data = {'username': 'new_username',
                'email': 'other@example.com',
                'password': 'cjdncdjnceawe'
                }
        request = self.factory.put(url, data, format='json')
        force_authenticate(request, user=self.user)  # Ensure the request is made by a different user
        response = self.view(request, pk=other_user.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDeleteAccount(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DeleteAccountView.as_view()
        self.user = UserModel.objects.create_user(
            username='test',
            password='test',
        )
        self.token = Token.objects.create(user=self.user)
        self.url = f'/api/accounts/delete/{self.user.pk}/'

    def test_delete_account_success(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.user.pk)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(UserModel.objects.filter(pk=self.user.pk).exists())

    def test_delete_account_permission_denied(self):
        other_user = UserModel.objects.create_user(username='other_user', email='email', password='password')
        url = f'/api/accounts/delete/{other_user.pk}/'
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=other_user.pk)

        self.assertEqual(response.status_code, 403)
