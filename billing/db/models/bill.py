import asyncio
import pprint
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, Column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, Field

from billing.db.connection import get_session
from billing.provider.common import ProviderType
from billing.provider.utils import get_provider
from billing.schemas.yapay.item import ItemType
from billing.schemas.yapay.operation import OperationType, OperationStatus
from billing.schemas.yapay.order.response import OrderResponse
from billing.schemas.yapay.payment import CurrencyCode, PaymentStatus, ResponseStatus


class CommonModelFields(SQLModel):
    id: UUID = Field(default=uuid.uuid4(), primary_key=True)
    created: datetime
    updated: datetime


class ItemQuantity(CommonModelFields, table=True):
    """Количество товара в заказе."""
    available: Optional[float] = None
    count: float
    label: Optional[str] = None


class CartItem(CommonModelFields, table=True):
    productId: UUID
    # quantity: ItemQuantity
    item_quantity_id: UUID = Field(default=None, foreign_key='itemquantity.id')
    discountedUnitPrice: Optional[float] = None
    finalPrice: Optional[float] = None
    # measurements: Measurements | None = None
    # receipt: ItemReceipt | None = None
    subtotal: Optional[float] = None
    title: Optional[str] = None
    total: Optional[float] = None
    type: Optional[ItemType] = ItemType.UNSPECIFIED
    unitPrice: Optional[float] = None


class Cart(CommonModelFields, table=True):
    """Корзина после оплаты с примененными скидками."""

    # items: list[CartItem]
    cartId: Optional[str] = None
    # coupons: list[Coupon] | None = None
    # discounts: list[Discount] | None = None
    externalId: Optional[str] = None
    # measurements: Measurements | None = None
    # total: CartTotal | None = None
    total: float = None
    # total: CartTotal | None = None


class CartCartItems(CommonModelFields, table=True):
    cart_item_id: UUID = Field(default=None, foreign_key='cartitem.id')
    cart_id: UUID = Field(default=None, foreign_key='cart.id')


class Order(CommonModelFields, table=True):
    # cart: Cart
    cart_id: UUID = Field(default=None, foreign_key='cart.id')
    currencyCode: CurrencyCode
    created: Optional[datetime] = None
    merchantId: Optional[UUID] = None
    # metadata: str | None = None
    orderAmount: Optional[float] = None
    orderId: Optional[UUID] = None
    # paymentMethod: PaymentMethod | None = None
    paymentStatus: Optional[PaymentStatus] = None
    paymentUrl: Optional[str] = None
    reason: Optional[str] = None
    # shippingMethod: ShippingMethod | None = None
    updated: Optional[datetime] = None


class Operation(CommonModelFields, table=True):
    amount: float
    approvalCode: Optional[str] = None
    created: Optional[datetime] = None
    externalOperationId: Optional[str] = None
    operationId: UUID
    operationType: OperationType
    orderId: UUID = Field(default=None, foreign_key='order.id')
    # params: Dict[str, Any] | None = None
    reason: Optional[str] = None
    status: Optional[OperationStatus] = OperationStatus.PENDING
    updated: Optional[str] = None


if __name__ == '__main__':
    async def main():
        yp = await get_provider(ProviderType.yapay)
        response: OrderResponse = await yp.payment_info(entity_id="c3073b9d-edd0-49f2-a28d-b7ded8ff9a8b")
        async for session in get_session():
            session: AsyncSession
            if response.status == ResponseStatus.SUCCESS:
                date_field = {"created": datetime.utcnow(), "updated": datetime.utcnow()}
                data = response.data
                order = data.order
                cart = order.cart
                for cart_item in cart.items:
                    print('>')
                    itemq_model = ItemQuantity.model_validate({**dict(cart_item.quantity), **date_field})
                    session.add(itemq_model)
                    await session.commit()
                    print(itemq_model.id)
                    cart_model = CartItem.model_validate({"item_quantity_id": itemq_model.id, **dict(cart_item), **date_field})
                    session.add(cart_model)
                cart_model = Cart.model_validate({**dict(cart), **date_field, "total": cart.total.amount})
                session.add(cart_model)

                pprint.pprint(dict(order))
                order_model = Order.model_validate({**dict(order), "cart_id": cart_model.id})
                session.add(order_model)

                await session.commit()

        print(response.model_dump_json(indent=2))

    asyncio.run(main())
