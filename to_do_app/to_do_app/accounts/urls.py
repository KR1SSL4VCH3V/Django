from django.urls import path, include

from to_do_app.accounts.views import SignUpView, SignInView, SignOutView, DetailsView, EditView, DeleteUserView

urlpatterns = (
    path('register/', SignUpView.as_view(), name='register'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('profile/<int:pk>/', include([
        path('', DetailsView.as_view(), name='details user'),
        path('update/', EditView.as_view(), name='update user'),
        path('delete/', DeleteUserView.as_view(), name='delete user'),
    ])),

)
