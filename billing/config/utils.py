from functools import lru_cache

from pydantic_settings import BaseSettings

from billing.provider.common import ProviderType
from billing.config.default import DefaultSettings, YandexPaySettings, UkassaSettings


@lru_cache
def get_settings() -> DefaultSettings:
    return DefaultSettings()


@lru_cache
def get_provider_settings(provider: ProviderType) -> BaseSettings:

    if provider == ProviderType.yapay:
        return YandexPaySettings()
    elif provider == ProviderType.ukassa:
        return UkassaSettings()

    return BaseSettings()  # fallback to default
