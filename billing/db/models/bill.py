import asyncio
import pprint
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, DateTime, Float, String, ForeignKey, Text, Table, Column, Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, relationship

from billing.db.connection import get_session
from billing.endpoints.examples.request import create_order_example
from billing.provider.common import ProviderType
from billing.provider.utils import get_provider
from billing.schemas.yapay.item import ItemType
from billing.schemas.yapay.operation import OperationType, OperationStatus
from billing.schemas.yapay.order.request import OrderRequest
from billing.schemas.yapay.order.response import OrderResponse
from billing.schemas.yapay.payment import CurrencyCode, ResponseStatus, PaymentStatus
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


# cart_item_table = Table(
#     "cart_item",
#     DeclarativeBase.metadata,
#     Column("item_id", ForeignKey("item.id"), primary_key=True),
#     Column("cart_id", ForeignKey("cart.id"), primary_key=True)
# )


class CartItem(DeclarativeBase, CommonFieldMixin):
    __tablename__ = "cart_item"

    cart_id: Mapped[UUID] = mapped_column(ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"), nullable=False)


# class CommonModelFields(SQLModel):
#     id: UUID = Field(default=uuid.uuid4(), primary_key=True)
#     created: datetime
#     updated: datetime


class ItemQuantity(CommonFieldMixin, DeclarativeBase):
    __tablename__ = "item_quantity"

    # available: Optional[float] = None
    available: Mapped[float] = mapped_column(Float, nullable=True)
    # count: float
    count: Mapped[float] = mapped_column(Float, nullable=False)
    # label: Optional[str] = None
    label: Mapped[str] = mapped_column(String(255), nullable=True)


# class ItemQuantity(CommonModelFields, table=True):
#     """Количество товара в заказе."""
#     available: Optional[float] = None
#     count: float
#     label: Optional[str] = None


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

# class CartItem(CommonModelFields, table=True):
#     productId: UUID
#     # quantity: ItemQuantity
#     item_quantity_id: UUID = Field(default=None, foreign_key='itemquantity.id')
#     discountedUnitPrice: Optional[float] = None
#     finalPrice: Optional[float] = None
#     # measurements: Measurements | None = None
#     # receipt: ItemReceipt | None = None
#     subtotal: Optional[float] = None
#     title: Optional[str] = None
#     total: Optional[float] = None
#     type: Optional[ItemType] = ItemType.UNSPECIFIED
#     unitPrice: Optional[float] = None


# class CartCartItems(CommonModelFields, table=True):
#     cart_item_id: UUID = Field(default=None, foreign_key='cartitem.id')
#     cart_id: UUID = Field(default=None, foreign_key='cart.id')


class Cart(CommonFieldMixin, DeclarativeBase):
    """Корзина после оплаты с примененными скидками."""

    __tablename__ = "cart"

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


# class Cart(CommonModelFields, table=True):
#     """Корзина после оплаты с примененными скидками."""
#
#     # items: list[CartItem]
#     cartId: Optional[str] = None
#     # coupons: list[Coupon] | None = None
#     # discounts: list[Discount] | None = None
#     externalId: Optional[str] = None
#     # measurements: Measurements | None = None
#     # total: CartTotal | None = None
#     total: float = None
#     # total: CartTotal | None = None


class Order(CommonFieldMixin, DeclarativeBase):
    __tablename__ = "order"

    # cart: Cart
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

# class Order(CommonModelFields, table=True):
#     # cart: Cart
#     cart_id: UUID = Field(default=None, foreign_key='cart.id')
#     currencyCode: CurrencyCode
#     created: Optional[datetime] = None
#     merchantId: Optional[UUID] = None
#     # metadata: str | None = None
#     orderAmount: Optional[float] = None
#     orderId: Optional[UUID] = None
#     # paymentMethod: PaymentMethod | None = None
#     paymentStatus: Optional[PaymentStatus] = None
#     paymentUrl: Optional[str] = None
#     reason: Optional[str] = None
#     # shippingMethod: ShippingMethod | None = None
#     updated: Optional[datetime] = None


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


if __name__ == '__main__':
    # async def main():
    #     yp = await get_provider(ProviderType.yapay)
    #     response: OrderResponse = await yp.payment_info(entity_id="c3073b9d-edd0-49f2-a28d-b7ded8ff9a8b")
    #     async for session in get_session():
    #         session: AsyncSession
    #         if response.status == ResponseStatus.SUCCESS:
    #             date_field = {"created": datetime.utcnow(), "updated": datetime.utcnow()}
    #             data = response.data
    #             order = data.order
    #             cart = order.cart
    #             for cart_item in cart.items:
    #                 print('>')
    #                 itemq_model = ItemQuantity.model_validate({**dict(cart_item.quantity), **date_field})
    #                 session.add(itemq_model)
    #                 await session.commit()
    #                 print(itemq_model.id)
    #                 cart_model = Item.model_validate(
    #                     {"item_quantity_id": itemq_model.id, **dict(cart_item), **date_field})
    #                 session.add(cart_model)
    #             cart_model = Cart.model_validate({**dict(cart), **date_field, "total": cart.total.amount})
    #             session.add(cart_model)
    #
    #             pprint.pprint(dict(order))
    #             order_model = Order.model_validate({**dict(order), "cart_id": cart_model.id})
    #             session.add(order_model)
    #
    #             await session.commit()
    #
    #     print(response.model_dump_json(indent=2))

    async def request():
        model = OrderRequest.model_validate(create_order_example)

        async for session in get_session():
            session: AsyncSession
            items = []
            for item in model.cart.items:
                item_q_model = ItemQuantity(**dict(item.quantity.model_dump()))
                session.add(item_q_model)
                await session.flush()

                data = {
                    **dict(item.model_dump(exclude={"quantity", }, exclude_none=True)),
                    "item_quantity_id": item_q_model.id,
                }
                item_model = Item(**data)
                items.append(item_model)

                session.add(item_model)
                await session.flush()

            cart_model = Cart(externalId=str(uuid.uuid4()), total=model.cart.total.amount, items=items)
            session.add(cart_model)
            await session.flush()

            order = Order(cart_id=cart_model.id, orderId=model.orderId)
            session.add(order)

            await session.commit()

            await session.refresh(cart_model)
            await session.refresh(order)

    asyncio.run(request())
