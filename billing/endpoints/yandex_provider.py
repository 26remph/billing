import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from billing.db.connection import get_session
from billing.db.models import Item, ItemQuantity, Cart, Order
from billing.endpoints.examples.request import create_order_example
from billing.endpoints.examples.webhook import webhook_example
from billing.esb.common import BillingAction, BillingSignal
from billing.esb.emitter import EsbBillingEmitter
from billing.provider.utils import get_provider
from billing.provider.yapay.payment import YandexPayment, PaymentInfoType
from billing.schemas.yapay.operation import OperationResponse
from billing.schemas.yapay.order.request import OrderRequest
from billing.schemas.yapay.order.response import OrderResponse, CreateOrderResponse
from billing.schemas.yapay.payment import PaymentStatus
from billing.schemas.yapay.webhook import WebhookV1Request, Event
from billing.services import get_esb_services

api_router = APIRouter(tags=["Yandex provider"])


@api_router.post("/pay", response_model=CreateOrderResponse)
async def create(
    model: OrderRequest = Body(..., example=create_order_example),
    session: AsyncSession = Depends(get_session),
    provider: YandexPayment = Depends(get_provider),
):
    """Логика работы ручки:

    Делаем запись в бэкэнд платежной системы, в случае успешного ответа:
        - получаем ссылку на оплату и статус ответа.
        - получаем текущее состояние заказа для записи в базу
        - записываем в базу биллинга информацию о платежной операции
        - возвращаем ссылку на оплату
    """

    request_id = str(uuid.uuid4())  # get from header over nginx
    response = await provider.create(model=model, idempotency_key=request_id)

    if response.code == 200:
        items = []
        for item in model.cart.items:
            item_q_model = ItemQuantity(**dict(item.quantity.model_dump()))
            session.add(item_q_model)
            await session.flush()

            data = {
                **dict(
                    item.model_dump(
                        exclude={
                            "quantity",
                        },
                        exclude_none=True,
                    )
                ),
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

    return response


@api_router.post("/webhook")
async def webhook(
    model: WebhookV1Request = Body(..., example=webhook_example),
    session: AsyncSession = Depends(get_session),
    esb: EsbBillingEmitter = Depends(get_esb_services),
):
    """Логика работы ручки.
    - Получаем статус входящего события и делаем апдейт в базе.
    - Обновляем самое позднее событие.
    В случае оплаты/возврата:
        - отправляем сообщение в шину для auth сервиса об прекращении
        или предоставлении доступа к фильму.

    """

    # use for one stage billing processing
    if model.event == Event.ORDER_STATUS_UPDATED:
        #  select for update database
        q = select(Order).where(Order.orderId == model.order.orderId).with_for_update()
        db_order: Order = await session.scalar(q)
        db_order.paymentStatus = model.order.paymentStatus
        db_order.updated = datetime.utcnow()
        await session.commit()

        # send signal in auth service to get access for content
        if model.order.paymentStatus == PaymentStatus.CAPTURED:
            q = select(Item, Cart).join(Cart.items).where(Cart.id == db_order.cart_id)
            result = await session.execute(q)
            items_uuid = [str(row.productId) for row in result.scalars()]
            signal = BillingSignal(
                user_id=str(uuid.uuid4()),  # get from token
                cart_items=items_uuid,
            )
            await esb.emit(signal=signal, action=BillingAction.allow_access)

    # use for two stage billing processing and partial refund
    if model.event == Event.OPERATION_STATUS_UPDATED:
        ...

    return {"status": "success"}


@api_router.get("/info/order/{order_id}", response_model=OrderResponse)
async def get_order_info(
    order_id: uuid.UUID = Path(...), provider: Annotated[YandexPayment, Depends(get_provider)] = None
):
    return await provider.payment_info(str(order_id), typeinfo=PaymentInfoType.ORDER)


@api_router.get("/info/operation_info/{external_operation_id}", response_model=OperationResponse)
async def get_operation_info(
    external_operation_id: uuid.UUID = Path(...), provider: Annotated[YandexPayment, Depends(get_provider)] = None
):
    return await provider.payment_info(str(external_operation_id), typeinfo=PaymentInfoType.OPERATION)


@api_router.post("/clearing")
async def clearing(
    session: AsyncSession = Depends(get_session), provider: Annotated[YandexPayment, Depends(get_provider)] = None
):
    """Логика работы ручки.

    Выбираем транзакции по которым выданы ссылки, но не произошла оплата.
    Сверяет их с данными платежного провайдера и производит отмену, либо обновление статуса
    операции или всего заказа в базе сервиса.
    """
    return {"status": "success"}
