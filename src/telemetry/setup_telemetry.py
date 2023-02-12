from .telemetry import Telemetry


def setup_telemetry(app, settings):
    if settings.TELEMETRY_ENABLE:
        telemetry = Telemetry(app, settings)
        telemetry.fast_api_instrument()
        telemetry.async_pg_instrument()
        telemetry.redis_instrument()
