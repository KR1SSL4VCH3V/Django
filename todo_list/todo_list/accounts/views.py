from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics as rest_views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task_manager.accounts.serializers import RegisterSerializer, LogInSerializer, EditAccountSerializer

UserModel = get_user_model()


class RegisterView(rest_views.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'serializer': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogInView(rest_views.GenericAPIView):
    serializer_class = LogInSerializer
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request):
        user = authenticate(username=request.data['username'], password=request.data['password'])

        if user:
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class EditAccountView(rest_views.UpdateAPIView):
    queryset = UserModel
    serializer_class = EditAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        instance = get_object_or_404(UserModel, pk=pk)
        return instance

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if instance != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            instance.username = serializer.validated_data.get('username', instance.username)
            instance.email = serializer.validated_data.get('email', instance.email)

            if serializer.validated_data.get('new_password1'):
                instance.set_password(serializer.validated_data['new_password1'])
            instance.save()
            return Response({'message': 'Account updated successfully!'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(rest_views.DestroyAPIView):
    queryset = UserModel.objects.all()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
