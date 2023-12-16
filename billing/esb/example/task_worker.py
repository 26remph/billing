import asyncio

import aio_pika
from aio_pika import IncomingMessage
from aio_pika.abc import AbstractIncomingMessage

from billing.config import get_settings


async def on_message_simple(message: IncomingMessage):
    print(" [x] Received %r" % message.body)
    await asyncio.sleep(message.body.count(b'.'))
    print(" [x] Done")
    await message.ack()


async def on_message(message: AbstractIncomingMessage):

    async with message.process():
        print(f" [x] Received message {message!r}")
        await asyncio.sleep(message.body.count(b'.'))
        print(f"     Message body is: {message.body!r}")


async def main():
    connection = await aio_pika.connect(cfg.rabbitmq_dsn)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue('task_queue', durable=True)
        # await queue.consume(on_message, no_ack=True)
        await queue.consume(on_message)
        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()

if __name__ == '__main__':
    cfg = get_settings()
    asyncio.run(main())