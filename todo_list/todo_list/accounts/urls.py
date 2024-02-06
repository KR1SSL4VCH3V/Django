from django.urls import path

from task_manager.accounts.views import RegisterView, LogInView, EditAccountView, DeleteAccountView

urlpatterns = (
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LogInView.as_view(), name='login'),
    path('edit/<int:pk>/', EditAccountView.as_view(), name='edit'),
    path('delete/<int:pk>/', DeleteAccountView.as_view(), name='delete'),
)
