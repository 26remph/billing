import datetime
from enum import Enum

from pydantic import BaseModel

from billing.schemas.yapay.receipt import ItemReceipt


class DeliveryStatus(str, Enum):
    NEW = "NEW"
    ESTIMATING = "ESTIMATING"
    EXPIRED = "EXPIRED"
    READY_FOR_APPROVAL = "READY_FOR_APPROVAL"
    COLLECTING = "COLLECTING"
    PREPARING = "PREPARING"
    DELIVERING = "DELIVERING"
    DELIVERED = "DELIVERED"
    RETURNING = "RETURNING"
    RETURNED = "RETURNED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Time(BaseModel):
    end: str
    start: str


class Grid(BaseModel):
    duration: str
    end: str
    start: str
    step: str


class Value(BaseModel):
    end: str
    start: str


class TimeIntervals(BaseModel):
    grid: Grid
    type: str
    values: list[Value]


class CustomerChoice(BaseModel):
    date: str
    time: Time


class CourierOption(BaseModel):
    allowedPaymentMethods: list[str]
    amount: str
    category: str
    courierOptionId: str
    customerChoice: CustomerChoice
    fromDate: str
    fromTime: str
    provider: str
    receipt: ItemReceipt
    timeIntervals: TimeIntervals
    title: str
    toDate: str
    toTime: str
    type: str


class Location(BaseModel):
    latitude: int
    longitude: int


class ScheduleItem(BaseModel):
    fromTime: str
    label: str
    toTime: str


class PickupOption(BaseModel):
    address: str
    allowedPaymentMethods: list[str]
    amount: str
    description: str
    fromDate: str
    location: Location
    phones: list[str]
    pickupPointId: str
    provider: str
    receipt: ItemReceipt
    schedule: list[ScheduleItem]
    storagePeriod: int
    title: str
    toDate: str


class YandexDeliveryOption(BaseModel):
    allowedPaymentMethods: list[str]
    amount: str
    category: str
    fromDatetime: str
    receipt: ItemReceipt
    title: str
    toDatetime: str
    yandexDeliveryOptionId: str


class ShippingMethod(BaseModel):
    courierOption: CourierOption
    methodType: str
    pickupOption: PickupOption
    yandexDeliveryOption: YandexDeliveryOption


class Delivery(BaseModel):
    actualPrice: float = None
    created: datetime.datetime = None
    price: float
    status: DeliveryStatus = DeliveryStatus.NEW
    updated: datetime.datetime = None
