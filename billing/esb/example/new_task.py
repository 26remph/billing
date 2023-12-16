import asyncio
import sys

from aio_pika import connect, Message, DeliveryMode

from billing.config import get_settings


async def main() -> None:
    # Perform connection
    connection = await connect(cfg.rabbitmq_dsn)

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        message_body = b" ".join(
            arg.encode() for arg in sys.argv[1:]
        ) or b"Hello World!"

        message = Message(message_body, delivery_mode=DeliveryMode.PERSISTENT)
        # Sending the message
        await channel.default_exchange.publish(
            message,
            routing_key="task_queue",
        )
        print(f" [x] Sent {message_body!r}")

if __name__ == '__main__':
    cfg = get_settings()
    asyncio.run(main())
