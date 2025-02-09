from ..views import PartViewSet
from rest_framework.routers import DefaultRouter

part_router = DefaultRouter()
part_router.register('parts', PartViewSet, basename='parts')
