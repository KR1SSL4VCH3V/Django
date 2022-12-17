
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import views as auth_views, login, get_user_model
from django.views import generic as views

from todo_list.accounts.forms import NewUserForm
from todo_list.accounts.models import Profile

UserModel = get_user_model()


class SignUpView(views.CreateView):
    template_name = 'accounts/register.html'
    form_class = NewUserForm
    success_url = reverse_lazy('list')

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        login(request, self.object)

        return result


class SignInView(auth_views.LoginView):
    template_name = 'accounts/sign-in.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('list')


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('sign-in')


class EditAccountUser(views.UpdateView):
    model = Profile
    template_name = 'accounts/edit.html'
    fields = '__all__'
    context_object_name = 'user'
    success_url = reverse_lazy('list')


class DeleteAccount(views.DeleteView):
    model = Profile
    template_name = 'accounts/delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('register')

