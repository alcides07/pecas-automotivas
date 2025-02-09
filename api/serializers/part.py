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
