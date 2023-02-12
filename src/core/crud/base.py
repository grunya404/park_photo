from typing import Any, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from tortoise import models

ModelType = TypeVar("ModelType", bound=models.Model)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Args:
            model: A Tortoise ORM model class
        """
        self.model = model

    async def get(self, id: Any) -> Optional[ModelType]:
        return await self.model.get(id=id)

    async def get_all(self, offset: int = 0, limit: int = 100) -> List[ModelType]:
        return await self.model.all().offset(offset).limit(limit)

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        return await self.model.create(**obj_in.dict(exclude_unset=True))

    async def update(self, db_obj: ModelType, obj_in: Union[UpdateSchemaType]) -> ModelType:
        await self.model.filter(id=db_obj.id).update(**obj_in.dict(exclude_unset=True))
        return await self.get(db_obj.id)

    async def remove(self, id: Any) -> bool:
        deleted_count = await self.model.filter(id=id).delete()
        if not deleted_count:
            return False
        return True
