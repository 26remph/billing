from enum import IntEnum

from pydantic import BaseModel, Base64Str


class ItemTax(IntEnum):
    """Налоговая ставка.
    https://pay.yandex.ru/ru/docs/custom/fns#tax"""

    nds_20 = 1
    nds_10 = 2
    nds_20_120 = 3
    nds_10_110 = 4
    nds_0 = 5
    without_nds = 6


class ItemMeasure(IntEnum):
    """Единицы измерения.
    https://pay.yandex.ru/ru/docs/custom/fns#measure-code
    """

    pc = 1
    g = 10
    kg = 11
    t = 12
    cm = 20
    dm = 21
    m = 22
    cm2 = 30
    dm2 = 31
    m2 = 32
    mm = 40
    l = 41
    m3 = 42
    kWh = 50
    Gkal = 51
    d = 70
    h = 71
    min = 72
    s = 73
    KiB = 80
    MiB = 81
    GiB = 82
    TiB = 83
    null = 255


class Supplier(BaseModel):
    inn: str
    name: str
    phones: list[str]


class MarkQuantity(BaseModel):
    denominator: int
    numerator: int


class PaymentsOperator(BaseModel):
    phones: list[str]


class TransferOperator(BaseModel):
    address: str
    inn: str
    name: str
    phones: list[str]


class Agent(BaseModel):
    agentType: int
    operation: str
    paymentsOperator: PaymentsOperator
    phones: list[str]
    transferOperator: TransferOperator


class ItemReceipt(BaseModel):
    """Данные для формирования чека."""

    agent: Agent = None
    excise: float
    markQuantity: MarkQuantity = None
    measure: ItemMeasure = None
    paymentMethodType: int = None
    paymentSubjectType: int = None
    productCode: Base64Str
    supplier: Supplier = None
    tax: ItemTax
    title: str = None
