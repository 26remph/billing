from aio_pika.abc import AbstractRobustConnection
from fastapi import Depends

from billing.esb.connection import get_rabbit_connection
from billing.esb.emitter import EsbBillingEmitter


async def get_esb_services(
        rabbit_connection: AbstractRobustConnection = Depends(get_rabbit_connection)
) -> EsbBillingEmitter:
    return EsbBillingEmitter(rabbit_connection)
