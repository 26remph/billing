import pprint
import uuid
from typing import Annotated

from aio_pika.abc import AbstractRobustConnection
from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from billing.db.connection import get_session
from billing.endpoints.examples.request import create_order_example
from billing.endpoints.examples.webhook import webhook_example
from billing.esb.connection import get_rabbit_connection
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
        provider: YandexPayment = Depends(get_provider)
):
    """Логика работы ручки:

    Делаем запись в бэкэнд платежной системы, в случае успешного ответа:
        - получаем ссылку на оплату и статус ответа.
        - получаем текущее состояние заказа для записи в базу
        - записываем в базу биллинга информацию о платежной операции
        - возвращаем ссылку на оплату
    """

    request_id = str(uuid.uuid4())
    response = await provider.create(model=model, idempotency_key=request_id)

    if response.code == 200:
        print("paymentUrl:", response.data.paymentUrl)
        pprint.pprint(response.model_dump(mode="json"))

    return response


@api_router.post("/webhook")
async def webhook(
        model: WebhookV1Request = Body(..., example=webhook_example),
        session: AsyncSession = Depends(get_session),
        esb: EsbBillingEmitter = Depends(get_esb_services)
):
    """Логика работы ручки.
    - Получаем статус входящего события и делаем апдейт в базе.
    - Обновляем самое позднее событие.
    В случае оплаты/возврата:
        - отправляем сообщение в шину для auth сервиса об прекращении
        или предоставлении доступа к фильму.

    """
    if model.event == Event.ORDER_STATUS_UPDATED:
        #  update database

        # send signal in
        if model.order.paymentStatus == PaymentStatus.CAPTURED:

        ...

    if model.event == Event.OPERATION_STATUS_UPDATED:
        ...

    return {"status": "success"}


@api_router.get("/info/order/{order_id}", response_model=OrderResponse)
async def get_order_info(
        order_id: uuid.UUID = Path(...),
        provider: Annotated[YandexPayment, Depends(get_provider)] = None
):
    return await provider.payment_info(str(order_id), typeinfo=PaymentInfoType.ORDER)


@api_router.get("/info/operation_info/{external_operation_id}", response_model=OperationResponse)
async def get_operation_info(
    external_operation_id: uuid.UUID = Path(...),
    provider: Annotated[YandexPayment, Depends(get_provider)] = None
):
    return await provider.payment_info(str(external_operation_id), typeinfo=PaymentInfoType.OPERATION)


@api_router.post("/clearing")
async def clearing(
        session: AsyncSession = Depends(get_session),
        provider: Annotated[YandexPayment, Depends(get_provider)] = None
):
    """Логика работы ручки.

    Выбираем транзакции по которым выданы ссылки, но не произошла оплата.
    Сверяет их с данными платежного провайдера и производит отмену, либо обновление статуса
    операции или всего заказа в базе сервиса.
    """
    return {"status": "success"}


