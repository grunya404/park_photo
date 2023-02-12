from fastapi import Depends
from fastapi_admin.app import app
from fastapi_admin.depends import get_current_admin, get_resources
from fastapi_admin.template import templates
from starlette.requests import Request

from config import settings


@app.get("/")
async def home(request: Request, resources=Depends(get_resources), curr_admin=Depends(get_current_admin)):
    return templates.TemplateResponse(
        "dashboard.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Dashboard",
            "page_pre_title": settings.SERVICE_NAME,
            "page_title": "Dashboard",
        },
    )
