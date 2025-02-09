from rest_framework import viewsets
from django.contrib.auth.models import User
from ..serializers import AdministradorReadSerializer, AdministradorWriteSerializer
from rest_framework.permissions import IsAuthenticated

class AdministradorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipular Administradores.
    """
    queryset = User.objects.filter(is_superuser=True)
    permission_classes = [IsAuthenticated]
    http_method_names=["get", "post"]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AdministradorReadSerializer
        return AdministradorWriteSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return []
        return super().get_permissions()
