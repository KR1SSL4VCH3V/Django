from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from todo_list.tasks.models import Task
from todo_list.tasks.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Task.objects.get(id=self.kwargs['pk'])
        except Task.DoesNotExist:
            raise Http404('Task does not exist!')

    def get_queryset(self):
        priority_task = Task.objects.filter(priority=True).order_by('-created_date')
        non_priority_task = Task.objects.filter(priority=False).order_by('-created_date')

        tasks = list(priority_task) + list(non_priority_task)

        return tasks
   
    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Successfully created task'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        print('updated')
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            print('object deleted')
        except Http404:
            print('not found after exception')
            return Response(status=status.HTTP_204_NO_CONTENT)
        print('not found')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
