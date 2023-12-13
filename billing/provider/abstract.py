import abc
from typing import Any

from pydantic import BaseModel


class AbstractRefund(abc.ABC):
    def __init__(self):
        self.client: Any = None

    @abc.abstractmethod
    def create(
        self,
        entity_id: str,
        body: BaseModel | dict[str, str],
        idempotency_key: str = None,
    ) -> BaseModel | dict[str, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def refund_info(self, entity_id: str) -> BaseModel | dict[str, str]:
        raise NotImplementedError


class AbstractPayment(abc.ABC):
    def __init__(self):
        self.client: Any = None

    @abc.abstractmethod
    def create(
        self, body: BaseModel | dict[str, str], idempotency_key: str = None
    ) -> BaseModel | dict[str, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def cancel(
        self,
        entity_id: str,
        body: BaseModel | dict[str, str],
        idempotency_key: str = None,
    ) -> BaseModel | dict[str, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def capture(
        self,
        entity_id: str,
        body: BaseModel | dict[str, str],
        idempotency_key: str = None,
    ) -> BaseModel | dict[str, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def payment_info(self, entity_id: str) -> BaseModel | dict[str, str]:
        raise NotImplementedError
