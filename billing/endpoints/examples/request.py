import uuid

from billing.config.default import YandexPaySettings
from billing.config.utils import get_provider_settings
from billing.provider.common import ProviderType

yapay_cfg: YandexPaySettings = get_provider_settings(ProviderType.yapay)

create_order = {
    "availablePaymentMethods": "CARD",
    "cart": {
        "items": [
            {
                "productId": str(uuid.uuid4()),
                "quantity": {"count": 1.0},
                "total": 1560.0
            }
        ],
        "total": {"amount": 1560.0}
    },
    "currencyCode": "RUB",
    "orderId": str(uuid.uuid4()),
    "redirectUrls": {"onError": yapay_cfg.redirect_on_error_url, "onSuccess": yapay_cfg.redirect_on_success_url},
}



