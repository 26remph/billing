from aio_pika import Message, DeliveryMode, ExchangeType
from aio_pika.abc import AbstractRobustConnection

from billing.config import get_settings
from billing.esb.common import BillingSignal, BillingAction


class EsbBillingEmitter:
    connection: AbstractRobustConnection

    def __init__(
        self,
        rabbit_connections: AbstractRobustConnection,
        queue_name: str = get_settings().rmq_queue_name,
        exchange_name: str = get_settings().rmq_exchange_name,
    ) -> None:
        self.connection = rabbit_connections
        self.queue_name = queue_name
        self.exchange_name = exchange_name

    async def emit(self, signal: BillingSignal, action: BillingAction):
        message_body = str(signal.model_dump(mode="python")).encode()

        async with self.connection:
            channel = await self.connection.channel()
            billing_exchange = await channel.declare_exchange(
                self.exchange_name,
                ExchangeType.DIRECT,
            )

            message = Message(
                message_body,
                delivery_mode=DeliveryMode.PERSISTENT,
            )

            await billing_exchange.publish(message, routing_key=action)
            print(f" [x] Sent {message!r}")
            print(f" [x] Sent body {message.body!r}")

