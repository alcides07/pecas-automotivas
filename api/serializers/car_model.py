from rest_framework import serializers
from api.models import CarModel

class CarModelReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = "__all__"

class CarModelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ("name", "manufacturer", "year")
