from rest_framework import generics as api_view, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from task_manager.tasks.models import Task
from task_manager.tasks.serializers import TaskSerializer


class HomeTaskView(api_view.ListAPIView):
    queryset = Task.objects.all().order_by('created_date')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_date')

    def list(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)
        return Response({'tasks': serializer.data}, status=status.HTTP_200_OK)


class CreateTaskView(api_view.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Successfully created task!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTaskView(api_view.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response({'message': 'Task was deleted!'}, status=status.HTTP_204_NO_CONTENT)
