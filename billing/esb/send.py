import asyncio

import aio_pika
from aio_pika import Message

from billing.config import get_settings


async def main():
    connection = await aio_pika.connect(cfg.rabbitmq_dsn)

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue("hello")

        await channel.default_exchange.publish(
            Message(b'Hello world'),
            routing_key=queue.name
        )

if __name__ == '__main__':
    cfg = get_settings()
    asyncio.run(main())