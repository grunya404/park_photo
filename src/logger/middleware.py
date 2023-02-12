from timeit import default_timer

from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from logger.logger import logger
from logger.utils import get_route_tempalte, get_user_agent


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_t = default_timer()

        response = await call_next(request)

        request_info = {
            "duration": round((default_timer() - start_t) * 1000),
            "http.status": response.status_code,
            "http.method": request.method,
            "http.target": request.url.path,
            "http.template": get_route_tempalte(request),
            "http.agent": get_user_agent(request),
        }
        await logger.info("request", **request_info)
        return response
