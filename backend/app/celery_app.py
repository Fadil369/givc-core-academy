"""Celery application configuration"""
from celery import Celery
from .config import settings

celery_app = Celery(
    "givc_academy",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Riyadh',
    enable_utc=True,
)

# Auto-discover tasks in the app
celery_app.autodiscover_tasks(['app.services'])
