import aio_pika

from billing.config import get_settings


async def main():
    connection = await aio_pika.connect(cfg.rabbitmq_dsn)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('hello')


if __name__ == '__main__':
    cfg = get_settings()
