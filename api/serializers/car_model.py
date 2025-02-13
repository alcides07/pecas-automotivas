from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import CarModel, Part
from ..serializers import PartReadSerializer

class CarModelReadSerializer(serializers.ModelSerializer):
    parts = PartReadSerializer(many=True, read_only=True)

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

        with transaction.atomic():
            for part in new_parts:
                if (part in instance.parts.all()):
                    raise ValidationError(f"{part.name} (ID {part.id}) já está associada a {instance.name} (ID {instance.id}).")

                if (part.quantity <= 0):
                    raise ValidationError(f"{part.name} (ID {part.id}) está sem estoque.")

                instance.parts.add(part)
                part.quantity -= 1
                part.save()

            return instance
        
class CarModelPartsDisassociateSerializer(serializers.ModelSerializer):
    parts = serializers.PrimaryKeyRelatedField(queryset=Part.objects.all(), many=True)

    class Meta:
        model = CarModel
        fields = "__all__"  

    def update(self, instance, validated_data):
        old_parts = validated_data.pop("parts", [])

        with transaction.atomic():
            for part in old_parts:
                if (part not in instance.parts.all()):
                    raise ValidationError(f"NÃO existe {part.name} (ID {part.id}) vinculado(a) a {instance.name} (ID {instance.id}).")

                instance.parts.remove(part)
                part.quantity += 1
                part.save()

            return instance

class CarModelPartsActionSerializer(serializers.Serializer):
    operation = serializers.ChoiceField(choices=["associate", "disassociate"], required=True)
    parts = serializers.PrimaryKeyRelatedField(queryset=Part.objects.all(), many=True, required=True)
