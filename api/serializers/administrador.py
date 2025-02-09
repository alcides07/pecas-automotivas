from rest_framework import serializers
from django.contrib.auth.models import User

class AdministradorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)

class AdministradorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        return user
