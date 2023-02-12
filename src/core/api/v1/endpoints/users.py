from typing import List

from fastapi import APIRouter, Depends, HTTPException

from core import crud, schemas
from core.api import deps

users_router = APIRouter(prefix="/users")


@users_router.get("/", response_model=List[schemas.User])
async def get_users(
    offset: int = 0, limit: int = 100, current_user: schemas.User = Depends(deps.get_current_active_superuser)
):
    return await crud.user.get_all(offset, limit)


@users_router.post("/", response_model=schemas.User)
async def create_user(
    new_user: schemas.UserCreate, current_user: schemas.User = Depends(deps.get_current_active_superuser)
):
    user = await crud.user.get_by_email(new_user.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    return await crud.user.create(new_user)


@users_router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int, current_user: schemas.User = Depends(deps.get_current_active_user)):
    user = await crud.user.get(user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user


@users_router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int, user_upd: schemas.UserUpdate, current_user: schemas.User = Depends(deps.get_current_active_superuser)
):
    user = await crud.user.get(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    return await crud.user.update(user_id, user_upd)


@users_router.delete("/{user_id}", response_model=schemas.ResponseModel)
async def delete_user(user_id: int, current_user: schemas.User = Depends(deps.get_current_active_superuser)):
    del_user = await crud.user.remove(user_id)
    return {"success": del_user}
