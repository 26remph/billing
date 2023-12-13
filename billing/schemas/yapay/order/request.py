
from pydantic import BaseModel, UUID4

from billing.schemas.yapay.cart import RenderedCart
from billing.schemas.yapay.common import PayMethod, CurrencyCode


class BillingReport(BaseModel):
    """Дополнительные параметры для отчета сплита."""

    branchId: str = None
    managerId: str = None


class QrData(BaseModel):
    """Дополнительные параметры для отправки ссылки на оплату с использованием QR."""

    token: str


class SmsOffer(BaseModel):
    """Дополнительные параметры для отправки ссылки на оплату с использованием SMS."""

    phone: str


class OrderExtensions(BaseModel):
    billingReport: BillingReport
    qrData: QrData
    smsOffer: SmsOffer


class MerchantRedirectUrls(BaseModel):
    """Ссылки для переадресации пользователя с формы оплаты. Обязательно для онлайн продавца."""

    onError: str
    onSuccess: str


class OrderRequestModel(BaseModel):
    """Основная модель запроса.

    :attribute
    availablePaymentMethods Доступные методы оплаты на платежной форме Яндекс Пэй Enum: CARD, SPLIT
    *cart Корзина
    *currencyCode Трехбуквенный код валюты заказа Enum: RUB
    extensions Дополнительные параметры для оформления оффлайн заказа
    *orderId Идентификатор заказа на стороне продавца (должен быть уникальным)
    purpose Назначение платежа
    *redirectUrls Ссылки для переадресации пользователя с формы оплаты. Обязательно для онлайн продавца
    ttl Время жизни заказа (в секундах) 180 <= ttl <= 60480 Default: 1800
    """

    availablePaymentMethods: PayMethod | list[PayMethod] = None
    cart: RenderedCart
    currencyCode: CurrencyCode
    extensions: OrderExtensions = None
    orderId: UUID4
    purpose: str = None
    redirectUrls: MerchantRedirectUrls
    ttl: int = 1800
