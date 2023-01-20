from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from todo_list.accounts.views import SignUpView, SignInView, SignOutView, DeleteAccount, EditAccountUser

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('edit/<int:pk>/', EditAccountUser.as_view(), name='edit'),
    path('delete/<int:pk>/', DeleteAccount.as_view(), name='delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
