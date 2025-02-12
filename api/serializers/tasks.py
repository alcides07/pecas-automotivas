from rest_framework import serializers
from celery.result import AsyncResult

class SimpleTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    message = serializers.CharField()

class TaskResultSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    status = serializers.CharField(required=False)
    result = serializers.CharField(required=False)

    def validate(self, data):
        task_id = data.get('task_id')
        task_result = AsyncResult(task_id)

        data['status'] = task_result.status
        data['result'] = str(task_result.result)
        
        return data
