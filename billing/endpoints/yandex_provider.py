import pprint
import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from billing.config import get_settings
from billing.db.connection import get_session
from billing.endpoints.examples.request import create_order_example
from billing.provider.utils import get_provider
from billing.provider.yapay.payment import YandexPayment, PaymentInfoType
from billing.schemas.yapay.operation import OperationResponse
from billing.schemas.yapay.order.request import OrderRequest
from billing.schemas.yapay.order.response import OrderResponse, CreateOrderResponse

api_router = APIRouter(tags=["Yandex payment provider"])
settings = get_settings()


@api_router.post("/pay", response_model=CreateOrderResponse)
async def create(
        model: OrderRequest = Body(..., example=create_order_example),
        session: AsyncSession = Depends(get_session),
        provider: YandexPayment = Depends(get_provider)
):
    """Логика работы ручки:

    Делаем запись в бэкэнд платежной системы, в случае успешного ответа:
        - возвращаем ссылку на оплату и статус ответа.
        - записываем в базу биллинга информацию о платежной операции
    """

    request_id = str(uuid.uuid4())
    response = await provider.create(model=model, idempotency_key=request_id)

    if response.code == 200:
        print("paymentUrl:", response.data.paymentUrl)
        pprint.pprint(response.model_dump(mode="json"))

    return response


@api_router.post("/webhook", response_model=...)
async def webhook(
        model: ... = Body(..., example=...),
        session: AsyncSession = Depends(get_session),
        provider: YandexPayment = Depends(get_provider)
):
    ...


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


