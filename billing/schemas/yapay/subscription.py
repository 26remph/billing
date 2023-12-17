from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SubscriptionStatus(str, Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class Subscription(BaseModel):
    customerSubscriptionId: UUID = Field(
        ...,
        description="ID подписки. Возвращается из SDK при успешном создании подписки. Также можно сохранить подписку при получении первой нотификации по ней. Дальнейшие обновления по этой подписке будут приходить с таким же значением этого поля.",
    )
    nextWriteOff: Optional[datetime] = Field(None, description="Дата следующей попытки списания денег по подписке")
    status: SubscriptionStatus = Field(..., description="Статус подписки")
    subscriptionPlanId: UUID = Field(
        ...,
        description="ID плана подписки, созданного в личном кабинете или через API.",
    )
