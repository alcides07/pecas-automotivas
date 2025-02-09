from ..views import AdministradorViewSet
from rest_framework.routers import DefaultRouter

administrador_router = DefaultRouter()
administrador_router.register('administradores', AdministradorViewSet, basename='administradores')
