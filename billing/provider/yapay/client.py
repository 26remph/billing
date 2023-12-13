import uuid
from typing import AsyncGenerator

import aiohttp
from aiohttp import ClientSession


class ApiClient:
    def __init__(self, api_key: str, request_timeout: int = 10_000):
        self.api_key = api_key
        self.request_timeout = request_timeout
        self.request_attempt = 0
        self.auth = f"Api-Key {api_key}"

    def create_header(self, request_id: str) -> dict[str, str]:
        return {
            "X-Request-Id": request_id,
            "X-Request-Timeout": str(self.request_timeout),
            "X-Request-Attempt": str(self.request_attempt),
            "Authorization": self.auth,
        }

    async def get_http_session(
        self, request_id: str = None
    ) -> AsyncGenerator[ClientSession, None]:
        if not request_id:
            request_id = str(uuid.uuid4())

        async with aiohttp.ClientSession(
            headers=self.create_header(request_id)
        ) as session:
            yield session
            await session.close()
