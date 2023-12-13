from fastapi import APIRouter

from billing.config import get_settings

api_router = APIRouter(tags=["Subscribe"])
settings = get_settings()
