from typing import Optional

from core import models, schemas
from core.crud.base import CRUDBase
from security import get_password_hash


class CRUDUser(CRUDBase[models.User, schemas.User, schemas.UserCreate, schemas.UserUpdate]):
    async def get_by_email(self, email: str) -> Optional[models.User]:
        result = await self.model.filter(email=email).first()
        if not result:
            return None
        return result

    async def create(self, new_user: schemas.UserCreate) -> models.User:
        if not new_user.username:
            new_user.username = new_user.email.split("@")[0]
        new_user.password = get_password_hash(new_user.password)
        new_user_model = await self.model.create(**new_user.dict(exclude_unset=True))
        return new_user_model

    async def update(self, id: int, obj_upd: schemas.UserUpdate) -> models.User:
        if obj_upd.password:
            obj_upd.password = get_password_hash(obj_upd.password)
        await self.model.filter(id=id).update(**obj_upd.dict(exclude_unset=True))
        return await self.get(id)


user = CRUDUser(models.User)
