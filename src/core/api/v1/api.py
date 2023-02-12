from fastapi import APIRouter

from core.api.v1.endpoints.login import login_router
from core.api.v1.endpoints.users import users_router

api_v1_router = APIRouter(prefix="/api/v1", tags=["Core"])

# api v1 routers
api_v1_router.include_router(users_router)
api_v1_router.include_router(login_router)
