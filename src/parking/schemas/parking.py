from typing import Optional, List

from pydantic import BaseModel
from pydantic.schema import datetime


class Parking(BaseModel):
    id: Optional[int] = None


class ParkingCreate(Parking):
    pass


class ParkingCounter(BaseModel):
    current_count: int
    updated_at: datetime


class ParkingPhoto(BaseModel):
    camera_id: int
    camera_title: str
    screenshot_url: str


class ParkingPhotoResponse(BaseModel):
    items: List[ParkingPhoto]
    date: Optional[str]
