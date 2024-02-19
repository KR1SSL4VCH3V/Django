from django.urls import path

from task_manager.tasks.views import HomeTaskView, DeleteTaskView, EditTaskView

urlpatterns = (
    path('home/', HomeTaskView.as_view(), name='home'),
    path('edit/<int:pk>/', EditTaskView.as_view(), name='edit'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete'),
)
