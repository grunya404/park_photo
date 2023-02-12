from fastapi import APIRouter

from .endpoints.parking import router

parking_api_v1_router = APIRouter(prefix="/api/v1", tags=["Parking"])

# api v1 routers
parking_api_v1_router.include_router(router)
