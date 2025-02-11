from rest_framework import serializers
from api.models import CarModel, Part

class CarModelReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = "__all__"

class CarModelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ("name", "manufacturer", "year")

class CarModelPartsAssociateSerializer(serializers.ModelSerializer):
    parts = serializers.PrimaryKeyRelatedField(queryset=Part.objects.all(), many=True)

    class Meta:
        model = CarModel
        fields = "__all__"  

    def update(self, instance, validated_data):
        new_parts = validated_data.get('parts', [])
        instance.parts.add(*new_parts)
        return instance
    
class CarModelPartsDisassociateSerializer(serializers.ModelSerializer):
    parts = serializers.PrimaryKeyRelatedField(queryset=Part.objects.all(), many=True)

    class Meta:
        model = CarModel
        fields = "__all__"  

    def update(self, instance, validated_data):
        old_parts = validated_data.pop("parts", [])
        instance.parts.remove(*old_parts)
        return instance

class CarModelPartsActionSerializer(serializers.Serializer):
    operation = serializers.ChoiceField(choices=["associate", "disassociate"], required=True)
    parts = serializers.PrimaryKeyRelatedField(queryset=Part.objects.all(), many=True, required=True)
