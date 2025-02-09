from ..views import CarModelViewSet
from rest_framework.routers import DefaultRouter

car_model_router = DefaultRouter()
car_model_router.register('car_models', CarModelViewSet, basename='car models')
