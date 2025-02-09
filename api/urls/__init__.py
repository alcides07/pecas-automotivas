from .part import part_router
from .user import user_router
from .car_model import car_model_router
from .administrador import administrador_router
from django.urls import include, path

urlpatterns = [
    path('', include(part_router.urls)),
    path('', include(user_router.urls)),
    path('', include(car_model_router.urls)),
    path('', include(administrador_router.urls)),
]