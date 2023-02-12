from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from admin.setup_admin import setup_admin
from config import settings
from core.api.v1.api import api_v1_router
from core.healthcheck.endpoints import healthcheck_router
from core.websocket.router import ws_router
from logger.setup_logging import setup_logging
from metrics.setup_metrics import setup_metrics
from parking.api.v1.api import parking_api_v1_router
from sentry.setup_sentry import setup_sentry
from telemetry.setup_telemetry import setup_telemetry

app = FastAPI(title=settings.SERVICE_NAME)

register_tortoise(app, config=settings.TORTOISE_CONFIG)


@app.on_event("startup")
async def startup():
    await setup_admin(app, settings)
    setup_logging(app)
    setup_sentry(app, settings)
    setup_telemetry(app, settings)
    setup_metrics(app, settings)


# mounts
app.mount("/static", StaticFiles(directory=settings.STATIC_ROOT), name="static")
app.mount("/screenshot", StaticFiles(directory=settings.SCREENSHOT_ROOT), name="screenshot")

# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(healthcheck_router)
app.include_router(api_v1_router)
app.include_router(ws_router)
app.include_router(parking_api_v1_router)
