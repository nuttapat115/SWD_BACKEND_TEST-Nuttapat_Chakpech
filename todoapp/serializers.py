from rest_framework import serializers
from todoapp.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_title', 'task_description', 'tast_status', 'due_date']