from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('task_manager.tasks.urls')),
    path('api/accounts/', include('task_manager.accounts.urls')),
]
