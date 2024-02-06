from django.urls import path

from task_manager.tasks.views import HomeTaskView, CreateTaskView, DeleteTaskView

urlpatterns = (
    path('home/', HomeTaskView.as_view(), name='home'),
    path('create/', CreateTaskView.as_view(), name='create'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete'),
)
