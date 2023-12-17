from logging import getLogger

from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import create_async_engine
from uvicorn import run

from billing.config import DefaultSettings
from billing.config.utils import get_settings
from billing.db.models.view import CartAdmin, OperationAdmin, OrderAdmin, CartItemAdmin
from billing.endpoints import list_of_routes
from billing.utils.common import get_hostname

logger = getLogger(__name__)


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.path_prefix)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Микросервис, реализующий возможность оплаты услуг кинотеатра."

    tags_metadata = [
        {"name": "Yandex provider", "description": "Yandex pay provider workflow."},
        {"name": "Health check", "description": "API health check."},
    ]

    application = FastAPI(
        title="Billing",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="1.0.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()

engine = create_async_engine(get_settings().database_uri, echo=True, future=True)
admin = Admin(app, engine)
admin.add_view(CartAdmin)
admin.add_view(CartItemAdmin)
admin.add_view(OrderAdmin)
admin.add_view(OperationAdmin)


if __name__ == "__main__":  # pragma: no cover
    settings_for_application = get_settings()
    run(
        "billing.__main__:app",
        host=get_hostname(settings_for_application.app_host),
        port=settings_for_application.app_port,
        reload=True,
        reload_dirs=["billing", "tests"],
        log_level="debug",
    )
