from fastapi import APIRouter
from fastapi.responses import JSONResponse
from tortoise import Tortoise

from core.schemas.response import ResponseModel

healthcheck_router = APIRouter(prefix="/healthcheck", tags=["Health check"])


@healthcheck_router.get(
    "/",
    responses={
        200: {
            "model": ResponseModel,
            "content": {"application/json": {"example": {"success": True, "msg": "App available"}}},
        }
    },
)
async def app_health_check():
    return {"success": True, "msg": "App available"}


@healthcheck_router.get(
    "/db",
    responses={
        200: {
            "model": ResponseModel,
            "content": {"application/json": {"example": {"success": True, "msg": "DB available"}}},
        },
        503: {
            "model": ResponseModel,
            "content": {"application/json": {"example": {"success": False, "msg": "DB unavailable"}}},
        },
    },
)
async def db_health_check():
    conn = Tortoise.get_connection("default")
    try:
        await conn.execute_query_dict("SELECT 1")
    except ConnectionRefusedError:
        return JSONResponse(status_code=503, content={"success": False, "msg": "DB unavailable"})
    return {"success": True, "msg": "DB available"}
