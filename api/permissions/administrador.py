from rest_framework.permissions import BasePermission

class IsAdministrador(BasePermission):
    """
    Permissão para verificar se é um administrador
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
