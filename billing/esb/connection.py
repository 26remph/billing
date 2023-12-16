import aio_pika
from aio_pika.abc import AbstractRobustConnection
from billing.config.utils import get_settings


async def get_rabbit_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(
        url=get_settings().rabbitmq_dsn,
    )
