from enum import Enum

from pydantic import BaseModel, UUID4

from billing.schemas.yapay.item import ItemQuantity, ItemType
from billing.schemas.yapay.receipt import ItemReceipt


class CouponStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    EXPIRED = "EXPIRED"
    null = "null"


class Coupon(BaseModel):
    description: str = None
    status: CouponStatus = None
    value: str


class Discount(BaseModel):
    amount: float
    description: str
    discountId: str


class Measurements(BaseModel):
    height: int
    length: int
    weight: int
    width: int


class CartTotal(BaseModel):
    """Стоимость всех товаров/услуг в корзине.

    :attribute
    amount Стоимость корзины с учетом всех скидок, и без учета доставки Example: 123.45
    """

    amount: float
    label: str | None = None


class CartItem(BaseModel):
    productId: UUID4
    quantity: ItemQuantity
    discountedUnitPrice: float | None = None
    finalPrice: float | None = None
    measurements: Measurements | None = None
    receipt: ItemReceipt | None = None
    subtotal: float | None = None
    title: str | None = None
    total: float | None = None
    type: ItemType = ItemType.UNSPECIFIED
    unitPrice: float | None = None


class Cart(BaseModel):
    """Корзина после оплаты с примененными скидками."""

    items: list[CartItem]
    cartId: str | None = None
    coupons: list[Coupon] | None = None
    discounts: list[Discount] | None = None
    externalId: str | None = None
    measurements: Measurements | None = None
    total: CartTotal | None = None


class RenderedCartItem(BaseModel):
    discountedUnitPrice: float = None
    productId: UUID4
    quantity: ItemQuantity
    receipt: ItemReceipt = None
    subtotal: float = None
    title: str = None
    total: float
    unitPrice: float = None


class RenderedCart(BaseModel):
    """Корзина для передачи на оплату."""

    externalId: UUID4 = None
    items: list[RenderedCartItem]
    total: CartTotal
