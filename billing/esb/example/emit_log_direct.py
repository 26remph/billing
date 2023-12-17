import asyncio
import sys

from aio_pika import DeliveryMode, ExchangeType, Message, connect

from billing.config import get_settings


async def main() -> None:
    # Perform connection
    connection = await connect(cfg.rabbitmq_dsn)

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        logs_exchange = await channel.declare_exchange(
            "logs",
            ExchangeType.DIRECT,
        )

        message_body = b" ".join(arg.encode() for arg in sys.argv[2:]) or b"Hello World!"

        message = Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        # Sending the message
        routing_key = sys.argv[1] if len(sys.argv) > 2 else "info"
        await logs_exchange.publish(message, routing_key=routing_key)

        print(f" [x] Sent {message!r}")
        print(f" [x] Sent {message.body!r}")


if __name__ == "__main__":
    cfg = get_settings()
    asyncio.run(main())
