from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from rest_framework import permissions

class IsUser(BasePermission):
    """
    Permissão para verificar se é um usuário comum'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS
