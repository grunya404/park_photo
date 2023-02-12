import structlog

from config import settings

logger = structlog.get_logger(settings.SERVICE_NAME)
