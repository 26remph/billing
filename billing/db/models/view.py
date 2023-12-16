from sqladmin import ModelView

from billing.db.models import Order, Cart, Item, Operation


class OperationAdmin(ModelView, model=Operation):
    column_list = [Operation.id]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id]


class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.id]


class CartItemAdmin(ModelView, model=Item):
    column_list = [Item.id]

