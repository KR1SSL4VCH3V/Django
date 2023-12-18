from rest_framework import generics as rest_views, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todo_list.accounts.serializers import SignUpSerializer, SignInSerializer, EditAccountSerializer

UserModel = get_user_model()


class SignUpView(rest_views.CreateAPIView):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SignInView(rest_views.GenericAPIView):
    serializer_class = SignInSerializer

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(rest_views.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            Token.objects.get(user=request.user).delete()
            print('The user is log out')
            return Response({'detail': 'Logged out successfully!'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'detail': 'User is not logged in!'}, status=status.HTTP_400_BAD_REQUEST)


class EditAccountView(rest_views.UpdateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = EditAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserModel, pk=pk)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            instance.username = serializer.validated_data.get('username', instance.username)
            instance.email = serializer.validated_data.get('email', instance.email)
            if serializer.validated_data.get('new_password1'):
                instance.set_password(serializer.validated_data['new_password1'])
            print(serializer)
            instance.save()
            return Response({'message': 'Account updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccount(rest_views.DestroyAPIView):
    queryset = UserModel.objects.all()
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserModel, pk=pk)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Account deleted successfully!'})

