import asyncio

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from billing.config import get_settings


async def on_message(message: AbstractIncomingMessage):
    print(" [x] Received message %r" % message)
    print("Message body is: %r" % message.body)

    print("Before sleep!")
    await asyncio.sleep(5)  # Represents async I/O operations
    print("After sleep!")


async def main():
    connection = await aio_pika.connect(cfg.rabbitmq_dsn)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('hello')
        await queue.consume(on_message, no_ack=True)
        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()

if __name__ == '__main__':
    cfg = get_settings()
    asyncio.run(main())
