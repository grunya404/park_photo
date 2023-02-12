import logging.config

import structlog

from config import settings
from logger.logger_config import logging_config
from logger.middleware import LoggingMiddleware
from logger.processors import (
    add_log_level,
    add_log_time,
    add_trace_span_id,
    render_to_logmsg,
)


def setup_logging(app):

    app.add_middleware(LoggingMiddleware)

    processors = [
        add_log_level,
        add_log_time,
        render_to_logmsg,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    if settings.TELEMETRY_ENABLE:
        processors.insert(0, add_trace_span_id)

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.config.dictConfig(logging_config)
