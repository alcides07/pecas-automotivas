from .part import part_router
from .user import user_router
from django.urls import include, path

urlpatterns = [
    path('', include(part_router.urls)),
    path('', include(user_router.urls)),
    # path('login/', MyTokenObtainPairView.as_view(), name='login'),
    # path('refresh/', MyTokenRefreshView.as_view(), name='refresh'),

]