from django.urls import path

from todo_list.tasks.views import TaskList, CreateTask, UpdateTaskView, DeleteTaskView

urlpatterns = (
    path('', TaskList.as_view(), name='list'),
    path('create/', CreateTask.as_view(), name='create'),
    path('update/<int:pk>/', UpdateTaskView.as_view(), name='update-task'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete-task'),
)
