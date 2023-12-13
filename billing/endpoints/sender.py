from fastapi import APIRouter, Depends, Body
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from billing.config import get_settings
from billing.db.connection import get_session

api_router = APIRouter(tags=["Sender"])
settings = get_settings()


class NewsLetterRequest:
    pass


@api_router.post(
    "/send_newsletter",
    status_code=status.HTTP_200_OK,
)
async def send_newsletter(
    body: dict = Body(
        ...,
        example={
            "url": "https://yandex.ru",
            "payload": {
                "title": "Новое письмо!",
                "text": "Произошло что-то интересное! :)",
                "image": "https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg",
            }
        }
    ),
    session: AsyncSession = Depends(get_session),
):
    ...