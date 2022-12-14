'''@$^QwErTyUiOp13579*'''
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, get_user_model
from django.views.generic import FormView


UserModel = get_user_model()


class SignUpView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

        return super(SignUpView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('list')
        return super(SignUpView, self).get(*args, **kwargs)


class SignInView(auth_views.LoginView):
    template_name = 'accounts/sign-in.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('list')


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('sign-in')


class DetailsView(views.DetailView):
    template_name = 'accounts/details.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.object

        return context


class EditView(views.UpdateView):
    template_name = 'accounts/update.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'email',)

    def get_success_url(self):
        return reverse_lazy('details', kwargs={
            'pk': self.request.user.pk,
        })


class DeleteUserView(views.DeleteView):
    template_name = 'accounts/delete.html'
    model = UserModel
    success_url = reverse_lazy('index')
