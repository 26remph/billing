from enum import Enum


class CardNetwork(str, Enum):
    """Платежная система."""

    AMEX = "AMEX"
    DISCOVER = "DISCOVER"
    JCB = "JCB"
    MASTERCARD = "MASTERCARD"
    MAESTRO = "MAESTRO"
    VISAELECTRON = "VISAELECTRON"
    VISA = "VISA"
    MIR = "MIR"
    UNIONPAY = "UNIONPAY"
    UZCARD = "UZCARD"
    HUMOCARD = "HUMOCARD"
    UNKNOWN = "UNKNOWN"
    UNDEFINED = "UNDEFINED"
    null = "null"


class PayMethod(str, Enum):
    CARD = "CARD"
    SPLIT = "SPLIT"
    SBP = "SBP"
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY"
    CARD_ON_DELIVERY = "CARD_ON_DELIVERY"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    AUTHORIZED = "AUTHORIZED"
    CAPTURED = "CAPTURED"
    VOIDED = "VOIDED"
    REFUNDED = "REFUNDED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    FAILED = "FAILED"
    null = "null"


class CurrencyCode(str, Enum):
    """Код валюты по ISO 4217"""

    RUB = "RUB"


class ResponseStatus(str, Enum):
    SUCCESS = "success"
