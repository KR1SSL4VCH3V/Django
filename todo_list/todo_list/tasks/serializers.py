from rest_framework import serializers

from task_manager.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(
        format='%d %b %Y',
        read_only=True,
    )
    due_date = serializers.DateField(
        format='%d %b %Y',
        error_messages={
            'invalid': 'This field may not be blank.'
        }
    )

    @staticmethod
    def get_due_date_message(obj):
        if obj.is_expired():
            return f"Task '{obj.title}' is due date and will be deleted automatically!"

        return ''

    class Meta:
        model = Task
        fields = ['pk', 'title', 'description', 'priority', 'created_date', 'due_date']

        user = serializers.PrimaryKeyRelatedField(
            read_only=True,
        )

    @staticmethod
    def validate_title(value):
        if Task.objects.filter(title=value).exists():
            raise serializers.ValidationError("Task with the same name already exists!")
        return value.capitalize()

    def to_internal_value(self, data):
        data['description'] = data.get('description', '').capitalize()
        return super(TaskSerializer, self).to_internal_value(data)
