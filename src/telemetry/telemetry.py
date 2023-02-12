from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)

from telemetry.instrumentor.redis import AsyncRedisInstrumentor


class Telemetry:
    def __init__(self, app, settings):
        self.settings = settings
        self.app = app

    @property
    def exporter(self) -> SpanExporter:
        if self.settings.TELEMETRY_DEBUG:
            return ConsoleSpanExporter()
        return JaegerExporter(
            agent_host_name=self.settings.TELEMETRY_AGENT_HOST,
            agent_port=int(self.settings.TELEMETRY_AGENT_PORT),
        )

    @property
    def resource(self) -> Resource:
        return Resource(attributes={"service.name": self.settings.SERVICE_NAME})

    @property
    def span_processor(self) -> BatchSpanProcessor:
        return BatchSpanProcessor(self.exporter)

    @property
    def tracer_provider(self) -> TracerProvider:
        tracer_provider = TracerProvider(resource=self.resource)
        trace.set_tracer_provider(tracer_provider)
        span_processor = BatchSpanProcessor(self.exporter)
        tracer_provider.add_span_processor(span_processor)
        return tracer_provider

    def fast_api_instrument(self):
        FastAPIInstrumentor.instrument_app(self.app, tracer_provider=self.tracer_provider)

    def async_pg_instrument(self):
        if all(
            [
                self.settings.POSTGRES_DB_HOST,
                self.settings.POSTGRES_DB_PORT,
                self.settings.POSTGRES_DB_USER,
                self.settings.POSTGRES_DB_PASSWORD,
                self.settings.POSTGRES_DB_NAME,
            ]
        ):
            AsyncPGInstrumentor().instrument()

    def redis_instrument(self):
        AsyncRedisInstrumentor().instrument()
