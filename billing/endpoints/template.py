from fastapi import APIRouter

from billing.config import get_settings

api_router = APIRouter(tags=["Template"])
settings = get_settings()