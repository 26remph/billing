import asyncio
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, DateTime, Float, String, ForeignKey, Text, Enum, select
from sqlalchemy.orm import mapped_column, Mapped, relationship

from billing.schemas.yapay.item import ItemType
from billing.schemas.yapay.operation import OperationType, OperationStatus
from billing.schemas.yapay.payment import CurrencyCode, PaymentStatus
from billing.db import DeclarativeBase


class CommonFieldMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, nullable=False, default=uuid.uuid4)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class CartItem(DeclarativeBase, CommonFieldMixin):
    __tablename__ = "cart_item"

    cart_id: Mapped[UUID] = mapped_column(ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"), nullable=False)


class ItemQuantity(CommonFieldMixin, DeclarativeBase):
    __tablename__ = "item_quantity"

    # available: Optional[float] = None
    available: Mapped[float] = mapped_column(Float, nullable=True)
    # count: float
    count: Mapped[float] = mapped_column(Float, nullable=False)
    # label: Optional[str] = None
    label: Mapped[str] = mapped_column(String(255), nullable=True)


class Item(CommonFieldMixin, DeclarativeBase):
    __tablename__ = "item"

    productId: Mapped[UUID] = mapped_column(nullable=False, default=uuid.uuid4)
    # productId: UUID
    # quantity: ItemQuantity
    item_quantity_id: Mapped[UUID] = mapped_column(ForeignKey("item_quantity.id", ondelete="CASCADE"), nullable=False)
    # item_quantity_id: UUID = Field(default=None, foreign_key='itemquantity.id')
    # discountedUnitPrice: Optional[float] = None
    discountedUnitPrice: Mapped[float] = mapped_column(Float, nullable=True)
    # finalPrice: Optional[float] = None
    finalPrice: Mapped[float] = mapped_column(Float, nullable=True)
    # measurements: Measurements | None = None
    # receipt: ItemReceipt | None = None
    subtotal: Mapped[float] = mapped_column(Float, nullable=True)
    # subtotal: Optional[float] = None
    title: Mapped[str] = mapped_column(Text, nullable=True)
    # title: Optional[str] = None
    # total: Optional[float] = None
    total: Mapped[float] = mapped_column(Float, nullable=True)
    # type: Optional[ItemType] = ItemType.UNSPECIFIED
    type: Mapped[str] = mapped_column(Enum(ItemType), default=ItemType.UNSPECIFIED)
    # unitPrice: Optional[float] = None
    unitPrice: Mapped[float] = mapped_column(Float, nullable=True)
    carts: Mapped[list["Cart"]] = relationship(
        secondary="cart_item", back_populates="items", lazy="selectin"
    )


class Cart(CommonFieldMixin, DeclarativeBase):
    """Корзина после оплаты с примененными скидками."""

    __tablename__ = "cart"

    order: Mapped[list["Order"]] = relationship(back_populates="cart", lazy="selectin")
    # items: list[CartItem]
    # cartId: Optional[str] = None
    cartId: Mapped[str] = mapped_column(String(255), nullable=True)
    # coupons: list[Coupon] | None = None
    # discounts: list[Discount] | None = None
    # externalId: Optional[str] = None
    externalId: Mapped[str] = mapped_column(String(255), nullable=True)
    # measurements: Measurements | None = None
    # total: CartTotal | None = None
    total: Mapped[float] = mapped_column(Float, nullable=True)
    # total: CartTotal | None = None
    items: Mapped[list["Item"]] = relationship(
        secondary="cart_item", back_populates="carts", lazy="selectin"
    )


class Order(CommonFieldMixin, DeclarativeBase):
    __tablename__ = "order"

    # cart: Cart
    cart: Mapped[list["Cart"]] = relationship(back_populates="order", lazy="selectin")
    cart_id: Mapped[UUID] = mapped_column(ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)
    # cart_id: UUID = Field(default=None, foreign_key='cart.id')
    # currencyCode: CurrencyCode
    currencyCode: Mapped[str] = mapped_column(Enum(CurrencyCode), nullable=False, default=CurrencyCode.RUB)
    # created: Optional[datetime] = None
    merchantId: Mapped[UUID] = mapped_column(default=uuid.uuid4, nullable=True)
    # merchantId: Optional[UUID] = None
    # metadata: str | None = None
    # orderAmount: Optional[float] = None
    orderAmount: Mapped[float] = mapped_column(Float, nullable=True)
    orderId: Mapped[UUID] = mapped_column(nullable=True, default=uuid.uuid4)
    # orderId: Optional[UUID] = None
    # paymentMethod: PaymentMethod | None = None
    # paymentStatus: Optional[PaymentStatus] = None
    paymentStatus: Mapped[str] = mapped_column(Enum(PaymentStatus), nullable=True)
    # paymentUrl: Optional[str] = None
    paymentUrl: Mapped[str] = mapped_column(Text, nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    # shippingMethod: ShippingMethod | None = None
    # updated: Optional[datetime] = None


class Operation(CommonFieldMixin, DeclarativeBase):

    __tablename__ = "operation"

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    # amount: float
    approvalCode: Mapped[str] = mapped_column(String(255), nullable=True)
    # approvalCode: Optional[str] = None
    # created: Optional[datetime] = None
    externalOperationId: Mapped[str] = mapped_column(String(255), nullable=True)
    operationId: Mapped[UUID] = mapped_column(nullable=False, default=uuid.uuid4)
    # operationId: UUID
    # operationType: OperationType
    operationType: Mapped[str] = mapped_column(Enum(OperationType))
    # orderId: UUID = Field(default=None, foreign_key='order.id')
    orderId: Mapped[UUID] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"), nullable=False)
    # params: Dict[str, Any] | None = None
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    # reason: Optional[str] = None
    status: Mapped[str] = mapped_column(Enum(OperationStatus), default=OperationStatus.PENDING)
    # status: Optional[OperationStatus] = OperationStatus.PENDING
    # updated: Optional[str] = None
