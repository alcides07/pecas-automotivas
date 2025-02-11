from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ..permissions import IsAdministrador, IsUser
from ..models import CarModel
from ..serializers import CarModelReadSerializer, CarModelWriteSerializer, CarModelPartsAssociateSerializer, CarModelPartsDisassociateSerializer, CarModelPartsActionSerializer
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

    @extend_schema(
        request=CarModelPartsActionSerializer, 
        responses=CarModelReadSerializer
    )
    @action(detail=True, methods=['patch'], permission_classes=[IsAdministrador])
    def parts(self, request, pk):
        """
        Endpoint para associar ou desassociar parts a um car model
        """
        operation = request.data.get("operation")

        if operation not in ["associate", "disassociate"]:
            return Response({"error": "Operation must be 'associate' or 'disassociate'."}, status=status.HTTP_400_BAD_REQUEST)
        
        car_model = get_object_or_404(CarModel, id=pk)        

        if operation == "associate":
            serializer = CarModelPartsAssociateSerializer(car_model, data=request.data, partial=True)
        elif operation == "disassociate":
            serializer = CarModelPartsDisassociateSerializer(car_model, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

