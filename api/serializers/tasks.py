from rest_framework import serializers

class SimpleTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    message = serializers.CharField()

