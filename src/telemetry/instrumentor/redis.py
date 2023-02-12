from typing import Collection

import aioredis
import wrapt
from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.semconv.trace import (
    DbSystemValues,
    NetTransportValues,
    SpanAttributes,
)
from opentelemetry.trace import SpanKind
from opentelemetry.trace.status import Status, StatusCode

__version__ = "0.0.1"


def _hydrate_span_from_args(connection, query_type, query) -> dict:
    span_attributes = {SpanAttributes.DB_SYSTEM: DbSystemValues.REDIS.value}

    redis_host = connection.connection_pool.connection_kwargs.get("host")
    redis_port = connection.connection_pool.connection_kwargs.get("port")

    span_attributes[SpanAttributes.NET_PEER_NAME] = redis_host
    span_attributes[SpanAttributes.NET_PEER_PORT] = redis_port
    span_attributes[SpanAttributes.NET_TRANSPORT] = NetTransportValues.IP_TCP.value
    span_attributes[SpanAttributes.DB_STATEMENT] = f"{query_type} {query}"

    return span_attributes


class AsyncRedisInstrumentor(BaseInstrumentor):
    def __init__(self):
        super().__init__()
        self._tracer = None

    def instrumentation_dependencies(self) -> Collection[str]:
        return ("aioredis >= 2.0.0",)

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        self._tracer = trace.get_tracer(__name__, __version__, tracer_provider)

        for method in ["Redis.execute_command"]:
            wrapt.wrap_function_wrapper("aioredis", method, self._do_execute)

    def _uninstrument(self, **__):
        for method in [
            "Redis.execute_command",
        ]:
            unwrap(aioredis, method)

    async def _do_execute(self, func, instance, args, kwargs):

        exception = None
        name = "redis"

        with self._tracer.start_as_current_span(name, kind=SpanKind.CLIENT) as span:
            if span.is_recording():
                span_attributes = _hydrate_span_from_args(
                    instance,
                    args[0],
                    args[1],
                )
                for attribute, value in span_attributes.items():
                    span.set_attribute(attribute, value)

            try:
                result = await func(*args, **kwargs)
            except Exception as exc:  # pylint: disable=W0703
                exception = exc
                raise
            finally:
                if span.is_recording() and exception is not None:
                    span.set_status(Status(StatusCode.ERROR))

        return result
