import datetime

from pydantic import BaseModel, UUID4

from billing.schemas.yapay.cart import Cart
from billing.schemas.yapay.payment import (
    CurrencyCode,
    PaymentStatus,
    CardNetwork,
    PayMethod,
    ResponseStatus,
)
from billing.schemas.yapay.delivery import Delivery, ShippingMethod
from billing.schemas.yapay.operation import Operation


class PaymentMethod(BaseModel):
    cardLast4: str | None = None
    cardNetwork: CardNetwork | None = None
    methodType: PayMethod


class Order(BaseModel):
    cart: Cart
    currencyCode: CurrencyCode
    created: datetime.datetime | None = None
    merchantId: UUID4 | None = None
    metadata: str | None = None
    orderAmount: float | None = None
    orderId: UUID4 | None = None
    paymentMethod: PaymentMethod | None = None
    paymentStatus: PaymentStatus | None = None
    paymentUrl: str | None = None
    reason: str | None = None
    shippingMethod: ShippingMethod | None = None
    updated: datetime.datetime | None = None

    # class Config:
    #     orm_mode = True


class OrderResponseData(BaseModel):
    delivery: Delivery | None = None
    operations: list[Operation] | None = None
    order: Order | None = None


class CreateOrderResponseData(BaseModel):
    paymentUrl: str


class OrderResponse(BaseModel):
    code: int | None = None
    data: OrderResponseData | None = None
    status: ResponseStatus | None = None


class CreateOrderResponse(BaseModel):
    code: int = None
    data: CreateOrderResponseData = None
    status: ResponseStatus = None


if __name__ == "__main__":
    # Test response model with url
    od = CreateOrderResponseData(paymentUrl="http://123.ru")
    orm = CreateOrderResponse(data=od)
