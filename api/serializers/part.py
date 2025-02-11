from rest_framework import serializers
from api.models import Part

class PartReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = "__all__"

class PartWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ("part_number", "name", "details", "price", "quantity")

class PartUploadFileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=255, allow_empty_file=False, use_url=False)

