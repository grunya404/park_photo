import structlog

from config import settings
from logger.processors import (
    add_log_level,
    add_log_time,
    add_trace_span_id,
    render_to_logmsg,
)

level = "DEBUG" if settings.DEBUG else "INFO"

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": [
                structlog.stdlib.add_logger_name,
                render_to_logmsg,
                add_log_level,
                add_log_time,
                add_trace_span_id,
            ],
            "keep_exc_info": True if settings.DEBUG else False,
        },
    },
    "handlers": {
        "json": {
            "level": level,
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "loggers": {
        settings.SERVICE_NAME: {
            "handlers": ["json"],
            "level": level,
        },
        "uvicorn": {"handlers": ["json"], "level": level},
        "uvicorn.error": {"handlers": ["json"], "level": level},
        "uvicorn.access": {
            "handlers": ["json"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

if settings.DEBUG:
    logging_config["loggers"].update(
        {
            "databases": {"handlers": ["json"], "level": level},
            "sqlaclhemy": {"handlers": ["json"], "level": level},
        }
    )
