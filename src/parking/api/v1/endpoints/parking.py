from fastapi import APIRouter, HTTPException, Depends
from fastapi.openapi.models import APIKey

from core.api.deps import get_api_key
from parking import crud, schemas

router = APIRouter(prefix="/parking")


@router.get("/screenshots", response_model=schemas.ParkingPhotoResponse)
async def get_screenshots(api_key: APIKey = Depends(get_api_key)):
    response = await crud.parking.get_camera_picture()
    if not response:
        raise HTTPException(
            status_code=400,
            detail="Не удалось получить данные скринов с камер",
        )
    return response

@router.get("/free_places", response_model=schemas.ParkingCounter)
async def get_free_places(api_key: APIKey = Depends(get_api_key)):
    response = await crud.parking.get_free_paces()
    if not response:
        raise HTTPException(
            status_code=400,
            detail="Данные о количестве мест устарели",
        )
    return response


@router.put("/free_places", response_model=schemas.ParkingCounter)
async def update_free_places(
        update_body: schemas.ParkingCounter,
        api_key: APIKey = Depends(get_api_key)
):
    response = await crud.parking.update_free_places(update_body)
    if not response:
        raise HTTPException(
            status_code=400,
            detail="Не удалось обновить счетчик мест парковки",
        )
    return response
