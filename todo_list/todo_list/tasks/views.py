import math

from rest_framework import generics as rest_api, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task_manager.tasks.models import Task
from task_manager.tasks.serializers import TaskSerializer


class HomeTaskView(rest_api.GenericAPIView):
    queryset = Task.objects.all().order_by('created_date')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_date')

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
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Successfully created task!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTaskView(rest_api.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.delete()
        return Response({'message': 'Task was deleted!'}, status=status.HTTP_204_NO_CONTENT)
