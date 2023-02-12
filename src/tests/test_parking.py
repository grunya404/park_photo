import datetime
from unittest import TestCase

import pytest
from httpx import AsyncClient

from main import app
from parking.schemas import ParkingCounter

FREE_PLACES = 1
FREE_PLACES_DATETIME = datetime.datetime.now()
headers = {"token": "token"}


class ParkingFreePlaceTesting(TestCase):

    @pytest.mark.asyncio
    async def test_a_update_fee_places(self):
        async with AsyncClient(app=app, base_url="http://localhost") as ac:
            request_body = ParkingCounter(current_count=FREE_PLACES, updated_at=FREE_PLACES_DATETIME).json()
            response = await ac.put(url="/api/v1/parking/free_places",
                                    headers=headers,
                                    data=request_body)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_fee_places(self):
        async with AsyncClient(app=app, base_url="http://localhost") as ac:
            response = await ac.get(url="/api/v1/parking/free_places",
                                    headers=headers, )
            response_json = response.json()
        assert response.status_code == 200
        assert response_json.current_count == FREE_PLACES
