from billing.endpoints.content import api_router as content_link_router
from billing.endpoints.mailing_list import api_router as mailing_list_router
from billing.endpoints.health_check import api_router as health_check_router
from billing.endpoints.yandex_provider import api_router as yapay_router
from billing.endpoints.template import api_router as template_router
from billing.endpoints.sender import api_router as sender_router


list_of_routes = [
    health_check_router,
    content_link_router,
    mailing_list_router,
    yapay_router,
    template_router,
    sender_router,
]


__all__ = [
    "list_of_routes",
]
