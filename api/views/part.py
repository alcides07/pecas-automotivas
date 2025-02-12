from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from api.tasks.import_parts import import_parts
from ..permissions import IsAdministrador, IsUser
from ..models import Part
from ..serializers import PartReadSerializer, PartWriteSerializer, PartUploadFileSerializer, SimpleTaskSerializer
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
        if self.action in ['parts_upload']:
            return PartUploadFileSerializer
        return PartWriteSerializer

    @extend_schema(
        request=PartUploadFileSerializer,
    )
    @action(detail=False, methods=['post'], permission_classes=[], url_path="upload")
    def parts_upload(self, request, pk=None):
        """
        Endpoint para upload de arquivo CSV de Parts.
        """
        serializer = PartUploadFileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            
            file_content = uploaded_file.read().decode('utf-8')
            
            result = import_parts.delay(file_content)
            
            response_data = {
                'task_id': result.id,
                'message': 'Arquivo recebido e processamento iniciado.'
            }
            
            response_serializer = SimpleTaskSerializer(data=response_data)
            response_serializer.is_valid(raise_exception=True)  
            
            return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
