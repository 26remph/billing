from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from billing.provider.abstract import AbstractPayment
from billing.provider.yapay.client import ApiClient
from billing.schemas.yapay.operation import OperationResponse
from billing.schemas.yapay.order.request import OrderRequestModel
from billing.schemas.yapay.order.response import OrderResponse, CreateOrderResponse


class PaymentInfoType(str, Enum):
    ORDER = "ORDER"
    OPERATION = "OPERATION"


class YandexPayment(AbstractPayment):
    def __init__(self, api_key: str, endpoint_cfg: BaseSettings):
        super().__init__()
        self.client: ApiClient = ApiClient(api_key=api_key)
        self.endpoint_cfg = endpoint_cfg

    async def create(
        self, model: OrderRequestModel, idempotency_key: str = None
    ) -> CreateOrderResponse:
        url = self.endpoint_cfg.order_create_url
        dump = model.model_dump(mode="json", exclude_none=True)

        async for session in self.client.get_http_session():
            async with session.post(url, json=dump) as response:
                body = await response.json()

        return CreateOrderResponse(**dict(body))

    async def cancel(self):
        ...

    async def capture(self):
        ...

    async def rollback(self):
        ...

    async def operation_info(self, external_operation_id: str) -> OperationResponse:
        url = f"{self.endpoint_cfg.operation_info_url}/{external_operation_id}"

        async for session in self.client.get_http_session():
            async with session.get(url) as response:
                body = await response.json()

        return OperationResponse(**dict(body))

    async def order_info(self, order_id: str) -> OrderResponse:
        url = f"{self.endpoint_cfg.order_info_url}/{order_id}"

        async for session in self.client.get_http_session():
            async with session.get(url) as response:
                body = await response.json()
        return OrderResponse(**dict(body))

    async def payment_info(
        self, entity_id, typeinfo: PaymentInfoType = PaymentInfoType.ORDER
    ) -> BaseModel:
        if typeinfo == PaymentInfoType.ORDER:
            model = await self.order_info(order_id=entity_id)
        else:
            model = await self.operation_info(external_operation_id=entity_id)

        return model
