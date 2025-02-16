from ..views import UserViewSet
from rest_framework.routers import DefaultRouter

user_router = DefaultRouter()
user_router.register('users', UserViewSet, basename='users')
