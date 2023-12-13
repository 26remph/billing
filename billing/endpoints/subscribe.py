import pprint
import uuid

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from billing.config import get_settings
from billing.db.connection import get_session
from billing.endpoints.examples.request import create_order_example
from billing.provider.utils import get_provider
from billing.provider.yapay.payment import YandexPayment
from billing.schemas.yapay.order.request import OrderRequest
from billing.schemas.yapay.order.response import OrderResponse, CreateOrderResponse

api_router = APIRouter(tags=["Subscribe"])
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


