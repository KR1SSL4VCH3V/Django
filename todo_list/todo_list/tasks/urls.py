from django.urls import include, path
from rest_framework import routers

from todo_list.tasks.views import TaskViewSet

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = (
    path('', include(router.urls)),
)
