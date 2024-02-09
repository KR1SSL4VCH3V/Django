from django.urls import path

from task_manager.tasks.views import HomeTaskView, DeleteTaskView

urlpatterns = (
    path('home/', HomeTaskView.as_view(), name='home'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete'),
)
