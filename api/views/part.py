from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..permissions import IsAdministrador, IsUser
from ..models import Part
from ..serializers import PartReadSerializer, PartWriteSerializer
from ..filters import PartFilter

class PartViewSet(viewsets.ModelViewSet):
    """
        ViewSet para manipular Parts
    """
    queryset = Part.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = PartReadSerializer
    permission_classes = [IsUser | IsAdministrador]
    filterset_class = PartFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PartReadSerializer
        return PartWriteSerializer

