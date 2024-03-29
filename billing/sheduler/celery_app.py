from celery import Celery
from kombu import Queue

from billing.config.utils import get_settings


settings = get_settings()

_name_ = "notify_celery"
celapp = Celery(
    broker=settings.celery_broker,
    backend=settings.redis_dsn,
    include=["billing.scheduler.clearing", "billing.scheduler.renewal"],
)

CELERY_CONFIG = {
    "task_default_queue": "default",
    "task_queues": (
        Queue("q_enrich_msg"),
        Queue("q_send_mail"),
        Queue("q_send_webdocket"),
    ),
    # 'task_serializer': 'pickle',
    "task_serializer": "json",
    "accept_content": ["json"],
    "result_serializer": "json",
    # 'accept_content': ['json', 'pickle'],
    "broker_connection_retry_on_startup": True,
}

celapp.conf.update(**CELERY_CONFIG)
