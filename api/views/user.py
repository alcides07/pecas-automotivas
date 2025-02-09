from rest_framework import viewsets
from django.contrib.auth.models import User
from ..serializers import UserReadSerializer, UserWriteSerializer
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipular users.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names=["get", "post"]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserReadSerializer
        return UserWriteSerializer

