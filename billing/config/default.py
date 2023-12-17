from pydantic import HttpUrl, RedisDsn
from pydantic_settings import BaseSettings


class UkassaSettings(BaseSettings):
    ...


class YandexPaySettings(BaseSettings):
    order_url: str = "https://sandbox.pay.yandex.ru/api/merchant/v1/orders"
    order_info_url: str = "https://sandbox.pay.yandex.ru/api/merchant/v1/orders"
    order_cancel_suffix: str = "cancel"
    order_refund_suffix: str = "refund"
    order_capture_suffix: str = "capture"
    order_rollback_suffix: str = "rollback"

    operation_info_url: str = "https://sandbox.pay.yandex.ru/api/merchant/v1/operations"

    redirect_on_error_url: str = "/error_page_url"
    redirect_on_success_url: str = "/success_page_url"

    request_timeout: int = 10_000
    api_key: str = "70c84fd3-7024-4b3c-84a3-f1d9ae1b1243"

    merchant_id: str | None = "70c84fd3-7024-4b3c-84a3-f1d9ae1b1243"
    client_id: str | None = None
    callback_url: str | None = None

    webhook_url: str = "https://sandbox.example.merchant.ru/v1/webhook"


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    env: str = "local"
    path_prefix: str = "/api/v1"
    app_host: str = "http://127.0.0.1"
    app_port: int = 8080

    postgres_db: str = "postgres"
    postgres_host: str = "localhost"
    postgres_user: str = "postgres"
    postgres_port: int = 5432
    postgres_password: str = "postgres"
    db_connect_retry: int = 20
    db_pool_size: int = 15
    engine_mode_echo: bool = True

    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_default_user: str = "rmuser"
    rabbitmq_default_pass: str = "password"
    rmq_exchange_name: str = "billing"
    rmq_queue_name: str = "billing_on"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_decode_responses: bool = True

    @property
    def celery_broker(self) -> HttpUrl:
        return self.rabbitmq_dsn

    @property
    def celery_backend(self) -> HttpUrl:
        return self.redis_dsn

    @property
    def redis_dsn(self) -> RedisDsn:
        """Get redis servers dsn for connection."""
        return f"redis://{self.redis_host}:{self.redis_port}?decode_responses={self.redis_decode_responses}"

    @property
    def rabbitmq_dsn(self) -> str:
        """Get rabbitmq servers dsn for connection."""
        return (
            f"amqp://{self.rabbitmq_default_user}:{self.rabbitmq_default_pass}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}/"
        )

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.postgres_db,
            "user": self.postgres_user,
            "password": self.postgres_password,
            "host": self.postgres_host,
            "port": self.postgres_port,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )
