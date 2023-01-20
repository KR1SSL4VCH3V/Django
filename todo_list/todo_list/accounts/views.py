from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views, login, get_user_model
from django.views import generic as views
from todo_list.accounts.forms import SignUpForm

UserModel = get_user_model()


class SignUpView(views.CreateView):
    template_name = 'accounts/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('list')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login(request, self.object)
        return response


# class SignUpView(views.CreateView):
#     template_name = 'accounts/register.html'
#     form_class = NewUserForm
#     success_url = reverse_lazy('list')
#
#     def form_valid(self, form):
#         result = super().form_valid(form)
#         login(self.request, self.object)
#
#         return result


class SignInView(auth_views.LoginView):
    template_name = 'accounts/sign-in.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('list')


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('sign-in')


class EditAccountUser(LoginRequiredMixin, views.UpdateView):
    model = UserModel
    template_name = 'accounts/edit.html'
    fields = '__all__'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse_lazy('edit', kwargs={
            'pk': self.request.user.pk,
        })


class DeleteAccount(LoginRequiredMixin, views.DeleteView):
    model = UserModel
    template_name = 'accounts/delete.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse_lazy('register')
