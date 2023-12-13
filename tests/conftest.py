# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from asyncio import get_event_loop_policy

import pytest
from httpx import AsyncClient

from billing.__main__ import get_app


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_app()
    yield AsyncClient(app=app, base_url="http://test")
