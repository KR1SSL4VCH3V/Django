from django.core.validators import validate_email
from rest_framework import serializers
from django.contrib.auth import get_user_model

from task_manager.accounts.validators import validate_password1, validate_username

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=30,
        required=True,
        validators=[validate_username]
    )

    email = serializers.EmailField(
        required=True,
        validators=[validate_email]
    )

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
    username = serializers.CharField(
        required=True
    )
    password = serializers.CharField(
        required=True
    )

    class Meta:
        model = UserModel
        fields = ('username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username:
            raise serializers.ValidationError('Username is required')

        if password:
            raise serializers.ValidationError('Password is required.')

        try:
            user = UserModel.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError('Invalid password')
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('User does not exist')


class EditAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=30,
        required=True,
        validators=[validate_username]
    )

    email = serializers.EmailField(
        required=True,
        validators=[validate_email]
    )

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
