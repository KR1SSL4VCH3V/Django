import datetime
import math
from copy import deepcopy

from django.db import IntegrityError
from django.utils import timezone
from rest_framework import generics as rest_api, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task_manager.tasks.models import Task
from task_manager.tasks.serializers import TaskSerializer


class HomeTaskView(rest_api.GenericAPIView):
    # queryset = Task.objects.all().order_by('priority')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Task.objects.filter(
                user=self.request.user,
                due_date__gte=timezone.now() - datetime.timedelta(weeks=2)).order_by('-priority'))

    def get(self, request):
        page_num = int(request.GET.get('page', 1))
        limit_num = int(request.GET.get('limit', 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get('search')
        tasks = Task.objects.all()
        total_tasks = tasks.count()

        if search_param:
            tasks = Task.objects.filter(title__icontains=search_param)

        serializer = self.serializer_class(tasks[start_num:end_num], many=True)

        return Response({
            'status': 'success',
            'total': total_tasks,
            'page': page_num,
            'last_page': math.ceil(total_tasks / limit_num),
            'tasks': serializer.data,
        })

    def post(self, request, *args, **kwargs):
        mutable_data = deepcopy(request.data)
        serializer = self.serializer_class(data=mutable_data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Successfully created task!'}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error': 'Task with the same title already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditTaskView(rest_api.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTaskView(rest_api.RetrieveDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response({'message': 'Task was deleted!'}, status=status.HTTP_204_NO_CONTENT)
