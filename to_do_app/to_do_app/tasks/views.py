from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic as views

from to_do_app.tasks.models import Task


class TaskList(LoginRequiredMixin, views.ListView):
    model = Task
    user = User
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['tasks'] = context['tasks'].filter(user=self.request.user)
        # context['count'] = context['count'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['tasks'] = search_input

        return context


class TaskDetails(LoginRequiredMixin, views.DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task-details.html'


class CreateTask(LoginRequiredMixin, views.CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('list')


class UpdateView(LoginRequiredMixin, views.UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('list')


class DeleteView(LoginRequiredMixin, views.DeleteView):
    model = Task

    context_object_name = 'task'
    success_url = reverse_lazy('list')
