"""Тестовый файл для демонстрации логики работы """
import asyncio
import pprint
import uuid

from billing.config.utils import get_provider_settings
from billing.provider.common import ProviderType
from billing.provider.yapay.payment import YandexPayment, PaymentInfoType
from billing.schemas.yapay.cart import RenderedCartItem, CartTotal, RenderedCart
from billing.schemas.yapay.payment import PayMethod, CurrencyCode
from billing.schemas.yapay.item import ItemQuantity
from billing.schemas.yapay.order.request import MerchantRedirectUrls, OrderRequest


async def main():
    # Создаем интерфейс оплаты с авторизацией по секретному ключу.
    ya_pay = YandexPayment(api_key=config.api_key, endpoint_cfg=config)

    # Создаем ключ идемпотентности, в нашем случае это идентификатор запроса.
    # Создаем сущность заказа в бэкэнде яндекс. Получаем ссылку на оплату.
    request_id = str(uuid.uuid4())
    response = await ya_pay.create(model=order, idempotency_key=request_id)

    if response.code == 200:
        print("paymentUrl:", response.data.paymentUrl)
        pprint.pprint(response.model_dump(mode="json"))

    await asyncio.sleep(10)

    # Проверяем статус заказа. Если успели перейти по ссылке и оплатить,
    # то по заказу появится операция в статусе CAPTURE

    response = await ya_pay.payment_info(order.orderId, typeinfo=PaymentInfoType.ORDER)
    print("info", response)
    for operation in response.data.operations:
        print(operation.operationId)
        print(operation.status)


if __name__ == "__main__":
    config = get_provider_settings(ProviderType.yapay)

    # Здесь создаем модель руками. В дальнейшем ее можно получить из PaymentApi
    # указав request_model == OrderRequest
    redirect_urls = MerchantRedirectUrls(
        onError=config.redirect_on_error_url, onSuccess=config.redirect_on_success_url
    )

    item = RenderedCartItem(
        productId=uuid.uuid4(), quantity=ItemQuantity(count=1), total=1560.00
    )
    cart = RenderedCart(items=[item], total=CartTotal(amount=1560.00))

    order = OrderRequest(
        availablePaymentMethods=PayMethod.CARD,
        cart=cart,
        currencyCode=CurrencyCode.RUB,
        orderId=uuid.uuid4(),
        redirectUrls=redirect_urls,
    )

    print(order.model_dump_json(indent=2, exclude_none=True))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
