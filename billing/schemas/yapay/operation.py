from enum import Enum
from typing import Dict, Any

from pydantic import BaseModel, UUID4
import datetime

from billing.schemas.yapay.payment import ResponseStatus


class OperationType(str, Enum):
    AUTHORIZE = "AUTHORIZE"
    REFUND = "REFUND"
    CAPTURE = "CAPTURE"
    VOID = "VOID"
    RECURRING = "RECURRING"


class OperationStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class Operation(BaseModel):
    amount: float
    approvalCode: str | None = None
    created: datetime.datetime | None = None
    externalOperationId: str | None = None
    operationId: UUID4
    operationType: OperationType
    orderId: UUID4
    params: Dict[str, Any] | None = None
    reason: str | None = None
    status: OperationStatus = OperationStatus.PENDING
    updated: str | None = None


class OperationResponseData(BaseModel):
    operation: Operation = None


class OperationResponse(BaseModel):
    code: int = None
    data: OperationResponseData = None
    status: ResponseStatus = None
