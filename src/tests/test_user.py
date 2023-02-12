import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_read_users():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get("/api/v1/users/")

    assert response.status_code == 401
