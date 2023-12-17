from billing.endpoints.health_check import api_router as health_check_router
from billing.endpoints.yandex_provider import api_router as yapay_router


list_of_routes = [
    health_check_router,
    yapay_router,
]


__all__ = [
    "list_of_routes",
]
