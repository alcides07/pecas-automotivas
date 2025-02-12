from ..views import TaskViewSet
from rest_framework.routers import DefaultRouter

task_router = DefaultRouter()
task_router.register('tasks', TaskViewSet, basename='tasks')
