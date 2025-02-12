from rest_framework import viewsets
from ..permissions import IsAdministrador
from ..serializers import TaskResultSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class TaskViewSet(viewsets.ViewSet):
    """
    View para visualizar o progresso de uma task
    """

    permission_classes = [IsAdministrador]

    @extend_schema(
        parameters=[
          OpenApiParameter("task_id", OpenApiTypes.STR), 
        ],
        request=OpenApiTypes.STR,
        responses=TaskResultSerializer,
    )
    def list(self, request):
        """
        Return o progresso de uma tarefa específica
        """
        task_id = request.query_params.get("task_id")
        
        serializer = TaskResultSerializer(data={"task_id": task_id})

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
