from billing.config.utils import get_provider_settings
from billing.provider.abstract import AbstractPayment
from billing.provider.common import ProviderType
from billing.provider.yapay.payment import YandexPayment


async def get_provider(provider_type: ProviderType) -> AbstractPayment:
    if provider_type == ProviderType.yapay:
        # Создаем интерфейс оплаты с авторизацией по секретному ключу.
        cfg = get_provider_settings(ProviderType.yapay)
        return YandexPayment(api_key=cfg.api_key, endpoint_cfg=cfg)
