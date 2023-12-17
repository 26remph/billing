# if __name__ == '__main__':
#     async def update():
#         model = WebhookV1Request.model_validate(webhook_example)
#         model.order.orderId = "c3073b9d-edd0-49f2-a28d-b7ded8ff9a8b"
#         q = select(Order).where(Order.orderId == "c3073b9d-edd0-49f2-a28d-b7ded8ff9a8b").with_for_update()
#         print(q)
#
#         async for session in get_session():
#             # session: AsyncSession
#             db_order: Order = await session.scalar(q)
#             print("db_order", db_order)
#             db_order.paymentStatus = model.order.paymentStatus
#             db_order.updated = datetime.utcnow()
#             await session.commit()
#             print("cart_id", db_order.cart_id)
#
#             q = select(Item, Cart).join(Cart.items).where(Cart.id == "411877c7-93e2-4a67-a8d8-fc7a47385a09")
#             print("q", q)
#             result = await session.execute(q)
#             # print("rows:", result.all())
#
#             # for row in result.scalars():
#             #     print('>1', row.productId)
#             item_uuid = [str(row.productId) for row in result.scalars()]
#             print('lst', item_uuid)


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

# async def request():
#     model = OrderRequest.model_validate(create_order_example)
#
#     async for session in get_session():
#         session: AsyncSession
#         items = []
#         for item in model.cart.items:
#             item_q_model = ItemQuantity(**dict(item.quantity.model_dump()))
#             session.add(item_q_model)
#             await session.flush()
#
#             data = {
#                 **dict(item.model_dump(exclude={"quantity", }, exclude_none=True)),
#                 "item_quantity_id": item_q_model.id,
#             }
#             item_model = Item(**data)
#             items.append(item_model)
#
#             session.add(item_model)
#             await session.flush()
#
#         cart_model = Cart(externalId=str(uuid.uuid4()), total=model.cart.total.amount, items=items)
#         session.add(cart_model)
#         await session.flush()
#
#         order = Order(cart_id=cart_model.id, orderId=model.orderId)
#         session.add(order)
#
#         await session.commit()
#
#         await session.refresh(cart_model)
#         await session.refresh(order)
#
# asyncio.run(update())
