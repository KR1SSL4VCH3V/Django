
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo_list.tasks.urls')),
    path('accounts/', include('todo_list.accounts.urls')),
]
