from rest_framework import serializers

from todo_list.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    is_priority = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    @staticmethod
    def get_is_priority(obj):
        return obj.priority

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if data['is_priority']:
            data['priority_flag'] = 'Priority task'

        else:
            data['priority_flag'] = 'Normal task'

        return data

