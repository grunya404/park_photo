from config import settings
from core.crud.base import CRUDBase
from parking import models, schemas
from redis.utils import get_object_from_redis, set_object_to_redis


class CRUDParking(CRUDBase[models.Camera,
                           schemas.Parking,
                           schemas.ParkingCreate,
                           schemas.ParkingCounter]):

    async def get_camera_picture(self, ) -> schemas.ParkingPhotoResponse:

        parking_photos = await get_object_from_redis(key=settings.CACHE_SCREEN_KEY, cls=schemas.ParkingPhotoResponse)
        if parking_photos:
            return parking_photos
        else:
            return None

    async def update_free_places(self, count: schemas.ParkingCounter) -> schemas.ParkingCounter:
        free_places = await get_object_from_redis(key=settings.CACHE_KEY_FREE_PLACE, cls=schemas.ParkingCounter)
        if not free_places:
            await set_object_to_redis(key=settings.CACHE_KEY_FREE_PLACE, schema=count, expires=settings.CACHE_TTL)
            free_places = count
        return free_places

    async def get_free_paces(self, ) -> schemas.ParkingCounter:
        free_places = await get_object_from_redis(key=settings.CACHE_KEY_FREE_PLACE, cls=schemas.ParkingCounter)
        return free_places


parking = CRUDParking(models.Camera)
