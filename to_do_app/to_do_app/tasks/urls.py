from django.urls import path

from to_do_app.tasks.views import TaskList, TaskDetails, CreateTask, UpdateView, DeleteView

urlpatterns = (
    path('', TaskList.as_view(), name='list'),
    path('details/<int:pk>/', TaskDetails.as_view(), name='details'),
    path('create/', CreateTask.as_view(), name='create'),
    path('update/<int:pk>/', UpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteView.as_view(), name='delete'),
)
