import datetime
from enum import Enum
from uuid import UUID

from sqlmodel import SQLModel, Field


class CommunicateChannel(str, Enum):
    EMAIL = "EMAIL"
    SOCIAL = "SOCIAL"
    WEBSOCKET = "WEBSOCKET"
    MOBILE = "MOBILE"


class DeliveryMode(str, Enum):
    EXPRESS = 'EXPRESS'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    BY_DATE = 'BY_DATE'


class TaskState(str, Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RETRY = "RETRY"
    REVOKED = "REVOKED"


class CommonModelFields(SQLModel):
    id: UUID = Field(default=None, primary_key=True)
    created: datetime.datetime
    modified: datetime.datetime


class TemplateStatic(CommonModelFields, table=True):
    template_id: UUID
    common_vars: str
    value: str


class Content(CommonModelFields, table=True):
    name: str = Field(max_length=50)
    template_id: UUID
    channel: CommunicateChannel
    delivery: DeliveryMode
    description: str


class SubscriberChanel(CommonModelFields, table=True):
    user_id: UUID
    channel: CommunicateChannel
    contact: str
    is_active: bool


class ContentUser(CommonModelFields, table=True):
    name: str = Field(max_length=255)
    content_id: UUID = Field(default=None, foreign_key="content.id")
    subscriber_channel_id: UUID = Field(default=None, foreign_key='subscriberchanel.id')


class Task(CommonModelFields, table=True):
    content_user_id: UUID = Field(default=None, foreign_key='contentuser.id')
    task_id: str
    state: TaskState






