import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pecas_automotivas.settings')
app = Celery('api')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
