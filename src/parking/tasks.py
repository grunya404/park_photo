import logging
import os
from datetime import datetime
from io import BytesIO

import aiofiles
import websockets
from aiobotocore.session import get_session
from websockets.exceptions import InvalidHeaderValue, ConnectionClosedError

from config import settings
from parking import schemas, models
from parking.schemas import ParkingPhotoResponse
from parking.video.video_processing import VideoProcessing
from redis.utils import set_object_to_redis

logger = logging.getLogger("tasks")


async def get_screenshots() -> ParkingPhotoResponse:
    print('starting cron creating screenshots')
    results = await models.Camera.all().limit(int(settings.LIMIT_CAMERAS))
    if not results or len(results) == 0:
        print('not found cameras rows, cron finish')
        return None
    parking_reponse = schemas.ParkingPhotoResponse(items=[])
    for result in results:
        screenshoter = VideoProcessing(stream_url=result.camera_url, camera_id=result.id)
        try:
            url = await screenshoter.get_screenshot()
        except Exception as e:
            print(f'cannot create screenshot from camera: {e}')
        parking_photo = schemas.ParkingPhoto(camera_id=result.id, screenshot_url=url,
                                             camera_title=result.camera_title_location)
        parking_reponse.items.append(parking_photo)
        session = get_session()
        async with session.create_client('s3', region_name=settings.AWS_S3_REGION_NAME,
                                         endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID) as client:

            async with  aiofiles.open(settings.BASE_DIR + parking_photo.screenshot_url) as f:
                file_data = BytesIO(f.buffer.read())
            await client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                    Key=parking_photo.screenshot_url,
                                    Body=file_data, ACL='public-read')
            os.remove(settings.BASE_DIR + parking_photo.screenshot_url)

    await set_object_to_redis(key=settings.CACHE_SCREEN_KEY, schema=parking_reponse, expires=settings.CACHE_TTL)
    print('finish cron job creating screenshots')


async def get_free_places():
    """
    !!disclamer
    получение свободных мест с контроллера парковки.

    На момент написания кода документация к этому контролеру и
    методам получения с него данных была крайне скудная.
    Единственным рабочим вариантом стал метод получения
    числа свободных мест из websocket. Переодически сбоит.
    Как поддерживать конеткт с websocket так и не разобрался, на любые команды сокет закрывается.
    # recv bytes: 0xff 0xa1 0xc2 0x0 0x1 0xfd

    # res: 253 161 194 0 1 253


    :return:
    """
    print("starting cron getting free places ")
    if not settings.PARKING_CONTROLLER_ENABLED:
        print("Сбор данных о свободных местах выключен")
        return None

    uri = settings.PARKING_CONTROLLER_WS_URL

    async with websockets.connect(uri) as websocket:
        try:
            controller_bytes = await websocket.recv()
            bta = bytearray(controller_bytes)
            # количество мест предположительно здесь
            decimal_count = int(bta[4])
            parking_counter = schemas.ParkingCounter(current_count=decimal_count, updated_at=datetime.now())
            await set_object_to_redis(key=settings.CACHE_KEY_FREE_PLACE, schema=parking_counter,
                                      expires=settings.CACHE_TTL)
            await websocket.close()
        except InvalidHeaderValue:
            print("error headers ws:// ")
        except ConnectionClosedError:
            print("connection close  ")
    print("finish cron getting free places ")
