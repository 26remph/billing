from enum import Enum

from pydantic import BaseModel


class ItemType(str, Enum):
    PHYSICAL = "PHYSICAL"
    DIGITAL = "DIGITAL"
    UNSPECIFIED = "UNSPECIFIED"


class ItemQuantity(BaseModel):
    """Количество товара в заказе."""

    available: float | None = None
    count: float
    label: str | None = None
