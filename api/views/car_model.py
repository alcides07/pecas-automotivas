from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..permissions import IsAdministrador, IsUser
from ..models import CarModel
from ..serializers import CarModelReadSerializer, CarModelWriteSerializer
from ..filters import CarModelFilter

class CarModelViewSet(viewsets.ModelViewSet):
    """
        ViewSet para manipular Car Models
    """
    queryset = CarModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = CarModelReadSerializer
    permission_classes = [IsUser | IsAdministrador]
    filterset_class = CarModelFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CarModelReadSerializer
        return CarModelWriteSerializer

