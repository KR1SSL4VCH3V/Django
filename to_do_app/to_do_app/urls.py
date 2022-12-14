from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('to_do_app.accounts.urls')),
    path('', include('to_do_app.tasks.urls')),

]
