from django.shortcuts import render
'''somepasssword2355'''
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic as views

from todo_list.tasks.models import Task


class TaskList(LoginRequiredMixin, views.ListView):
    model = Task
    user = User
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        return context


class CreateTask(LoginRequiredMixin, views.CreateView):
    model = Task
    fields = ['title', 'description', 'complete', ]
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class UpdateTaskView(LoginRequiredMixin, views.UpdateView):
    model = Task
    fields = ['title', 'description', 'complete', ]
    success_url = reverse_lazy('list')


class DeleteTaskView(LoginRequiredMixin, views.DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('list')
