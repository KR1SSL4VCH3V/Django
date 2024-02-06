from rest_framework import serializers
from django.contrib.auth import get_user_model

from task_manager.accounts.validators import validate_password1

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password1],
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, value):
        if value['password1'] != value['password2']:
            raise serializers.ValidationError('The passwords do not match!')
        return value

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
        )

        return user


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'password')


class EditAccountSerializer(serializers.ModelSerializer):
    new_password1 = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        validators=[validate_password1],
    )

    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'new_password1', 'new_password2']

    def validate(self, value):
        if value['new_password1'] != value['new_password2']:
            raise serializers.ValidationError('The passwords do not match!')
        return value

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            new_password=validated_data['new_password1'],
        )

        return user


