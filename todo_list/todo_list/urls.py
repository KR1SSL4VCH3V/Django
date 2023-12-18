from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('todo_list.tasks.urls')),
    path('api/accounts/', include('todo_list.accounts.urls')),
]
