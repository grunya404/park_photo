from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserCreate(UserBase):
    email: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: Optional[int] = None
