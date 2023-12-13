from pydantic_settings import BaseSettings


class UkassaSettings(BaseSettings):
    ...


class YandexPaySettings(BaseSettings):
    order_create_url: str = "https://sandbox.pay.yandex.ru/api/merchant/v1/orders"
    order_info_url: str = "https://sandbox.pay.yandex.ru/api/merchant/v1/orders"
    operation_info_url: str = (
        "https://sandbox.pay.yandex.ru/api/merchant/v1/operations"
    )

    redirect_on_error_url: str = "/error_page_url"
    redirect_on_success_url: str = "/success_page_url"

    request_timeout: int = 10_000
    api_key: str = "70c84fd3-7024-4b3c-84a3-f1d9ae1b1243"

    merchant_id: str | None = None
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

