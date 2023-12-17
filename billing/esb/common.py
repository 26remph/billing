from enum import Enum

from pydantic import BaseModel


class BillingAction(str, Enum):
    allow_access = "ALLOW_ACCESS"
    deny_access = "DENY_ACCESS"


class BillingSignal(BaseModel):
    user_id: str
    cart_items: list[str]
