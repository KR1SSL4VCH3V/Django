from rest_framework import serializers
import re
from django.contrib.auth import get_user_model


UserModel = get_user_model()
SPECIAL_CHARS = r"[!@#$%^&*(),.?\":{}|<>]"


class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']

    @staticmethod
    def validate_password1(value):

        if len(value) < 8:
            raise serializers.ValidationError('The password must be at least 8 characters!')

        if not re.search(r"\d", value):
            raise serializers.ValidationError('The password must contain at least one digit!')

        if not re.search('[A-Z]', value):
            raise serializers.ValidationError('The password must contain at least one capital letter!')

        if not re.search(SPECIAL_CHARS, value):
            raise serializers.ValidationError('The password must contain at least one special character!')

        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('The passwords do not match!')
        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
        )

        return user


class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'password')


class EditAccountSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
    )
    new_password1 = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8
    )

    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'old_password', 'new_password1', 'new_password2']

    @staticmethod
    def validate_password1(value):
        if len(value) < 8:
            raise serializers.ValidationError('The password must be at least 8 characters!')

        if not re.search(r"\d", value):
            raise serializers.ValidationError('The password must contain at least one digit!')

        if not re.search('[A-Z]', value):
            raise serializers.ValidationError('The password must contain at least one capital letter!')

        if not re.search(SPECIAL_CHARS, value):
            raise serializers.ValidationError('The password must contain at least one special character!')

        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
        print(user)
        if not user.check_password(value):
            raise serializers.ValidationError('Incorrect old password!')
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('The passwords do not match!')
        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            old_password=validated_data['old_password'],
            new_password=validated_data['new_password1'],
        )

        return user
