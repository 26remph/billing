import asyncio
import sys

from aio_pika import connect, Message, DeliveryMode, ExchangeType

from billing.config import get_settings


async def main() -> None:
    # Perform connection
    connection = await connect(cfg.rabbitmq_dsn)

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        logs_exchange = await channel.declare_exchange(
            "logs", ExchangeType.FANOUT,
        )

        message_body = b" ".join(
            arg.encode() for arg in sys.argv[1:]
        ) or b"Hello World!"

        message = Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        # Sending the message
        await logs_exchange.publish(message, routing_key="info")

        print(f" [x] Sent {message!r}")

if __name__ == '__main__':
    cfg = get_settings()
    asyncio.run(main())
