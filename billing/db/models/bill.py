import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import func, DateTime, Float, String, ForeignKey, Text, Enum
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

    available: Mapped[float] = mapped_column(Float, nullable=True)
    count: Mapped[float] = mapped_column(Float, nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=True)


class Item(CommonFieldMixin, DeclarativeBase):
    __tablename__ = "item"

    productId: Mapped[UUID] = mapped_column(nullable=False, default=uuid.uuid4)
    item_quantity_id: Mapped[UUID] = mapped_column(ForeignKey("item_quantity.id", ondelete="CASCADE"), nullable=False)
    discountedUnitPrice: Mapped[float] = mapped_column(Float, nullable=True)
    finalPrice: Mapped[float] = mapped_column(Float, nullable=True)
    subtotal: Mapped[float] = mapped_column(Float, nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=True)
    total: Mapped[float] = mapped_column(Float, nullable=True)
    type: Mapped[str] = mapped_column(Enum(ItemType), default=ItemType.UNSPECIFIED)
    unitPrice: Mapped[float] = mapped_column(Float, nullable=True)
    carts: Mapped[list["Cart"]] = relationship(secondary="cart_item", back_populates="items", lazy="selectin")


class Cart(CommonFieldMixin, DeclarativeBase):
    """Корзина после оплаты с примененными скидками."""

    __tablename__ = "cart"

    order: Mapped[list["Order"]] = relationship(back_populates="cart", lazy="selectin")
    cartId: Mapped[str] = mapped_column(String(255), nullable=True)
    externalId: Mapped[str] = mapped_column(String(255), nullable=True)
    total: Mapped[float] = mapped_column(Float, nullable=True)
    items: Mapped[list["Item"]] = relationship(secondary="cart_item", back_populates="carts", lazy="selectin")


class Order(CommonFieldMixin, DeclarativeBase):
    __tablename__ = "order"

    cart: Mapped[list["Cart"]] = relationship(back_populates="order", lazy="selectin")
    cart_id: Mapped[UUID] = mapped_column(ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)
    currencyCode: Mapped[str] = mapped_column(Enum(CurrencyCode), nullable=False, default=CurrencyCode.RUB)
    merchantId: Mapped[UUID] = mapped_column(default=uuid.uuid4, nullable=True)
    orderAmount: Mapped[float] = mapped_column(Float, nullable=True)
    orderId: Mapped[UUID] = mapped_column(nullable=True, default=uuid.uuid4)
    paymentStatus: Mapped[str] = mapped_column(Enum(PaymentStatus), nullable=True)
    paymentUrl: Mapped[str] = mapped_column(Text, nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)


class Operation(CommonFieldMixin, DeclarativeBase):
    __tablename__ = "operation"

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    approvalCode: Mapped[str] = mapped_column(String(255), nullable=True)
    externalOperationId: Mapped[str] = mapped_column(String(255), nullable=True)
    operationId: Mapped[UUID] = mapped_column(nullable=False, default=uuid.uuid4)
    operationType: Mapped[str] = mapped_column(Enum(OperationType))
    orderId: Mapped[UUID] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(Enum(OperationStatus), default=OperationStatus.PENDING)
