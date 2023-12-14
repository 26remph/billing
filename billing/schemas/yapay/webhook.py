from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from billing.schemas.yapay.payment import PaymentStatus
from billing.schemas.yapay.delivery import DeliveryStatus
from billing.schemas.yapay.operation import OperationType, OperationStatus
from billing.schemas.yapay.subscription import Subscription


class Event(str, Enum):
    TRANSACTION_STATUS_UPDATE = "TRANSACTION_STATUS_UPDATE"
    ORDER_STATUS_UPDATED = "ORDER_STATUS_UPDATED"
    OPERATION_STATUS_UPDATED = "OPERATION_STATUS_UPDATED"
    SUBSCRIPTION_STATUS_UPDATED = "SUBSCRIPTION_STATUS_UPDATED"


class OperationWebhookData(BaseModel):
    externalOperationId: Optional[str] = None
    operationId: UUID
    operationType: OperationType
    orderId: str
    status: OperationStatus


class OrderWebhookData(BaseModel):
    deliveryStatus: Optional[DeliveryStatus] = Field(
        None, description='Статусы доставки'
    )
    orderId: str = Field(
        ..., description='ID заказа, полученный в ответе /order/create'
    )
    paymentStatus: Optional[PaymentStatus] = Field(None, description='Статус заказа')


class WebhookV1Request(BaseModel):
    event: Event
    eventTime: datetime = Field(
        ..., description='время события в формате `RFC 3339`; `YYYY-MM-DDThh:mm:ssTZD`'
    )
    merchantId: UUID
    operation: Optional[OperationWebhookData] = None
    order: Optional[OrderWebhookData] = Field(
        None, description='если event == ORDER_STATUS_UPDATED'
    )
    subscription: Optional[Subscription] = Field(
        None,
        description='Состояние подписки. Передается, если event == SUBSCRIPTION_STATUS_UPDATED.',
    )