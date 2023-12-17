import datetime

from billing.schemas.yapay.operation import OperationStatus
from billing.schemas.yapay.webhook import Event

webhook_example = {
    "event": Event.ORDER_STATUS_UPDATED,
    "eventTime": datetime.datetime.now(),
    "merchantId": "c3073b9d-edd0-49f2-a28d-b7ded8ff9a8b",
    "order": {"deliveryStatus": "NEW", "orderId": "c3073b9d-edd0-49f2-a28d-b7ded8ff9a8b", "paymentStatus": "CAPTURED"},
}

webhook_operation_update_example = {
    "event": Event.OPERATION_STATUS_UPDATED,
    "eventTime": datetime.datetime.now(),
    "merchantId": "c3073b9d-edd0-49f2-a28d-b7ded8ff9a8b",
    "operation": {
        "externalOperationId": None,
        "operationId": "c3073b9d-edd0-49f2-a28d-b7ded8ff9a8b",
        "operationType": "CAPTURE",
        "orderId": "c3073b9d-edd0-49f2-a28d-b7ded8ff9a8b",
        "status": OperationStatus.SUCCESS,
    },
}
