from rest_framework import serializers

from task_manager.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['pk', 'title', 'description', 'priority', 'created_date']

        user = serializers.PrimaryKeyRelatedField(
            read_only=True,
        )

        @staticmethod
        def validate_name(value):
            if Task.objects.filter(title=value).exists():
                raise serializers.ValidationError("Task with the same name already exists!")
            return value

        @staticmethod
        def clean_title(value):
            return value.capitalize()
