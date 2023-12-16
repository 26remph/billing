from sqladmin import ModelView

from billing.db.models import Order, Cart, CartItem, Operation


class OperationAdmin(ModelView, model=Operation):
    column_list = [Operation.id]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id]


class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.id]


class CartItemAdmin(ModelView, model=CartItem):
    column_list = [CartItem.id]

