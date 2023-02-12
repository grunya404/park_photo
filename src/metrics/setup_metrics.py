from .app_http_request_latency_seconds import app_http_request_latency_seconds_metric
from .app_http_response_bytes_total import app_http_response_bytes_total_metric
from .app_http_response_error_count import app_http_response_error_count_metric
from .app_up import app_up_metric
from .instrumentator import FastApiInstrumentator


def setup_metrics(app, settings):
    if settings.METRICS_ENABLE:
        instrumentator = FastApiInstrumentator(
            excluded_handlers=[".*admin.*", "/metrics"],
            should_instrument_requests_inprogress=True,
            inprogress_name="app_http_request_inflight_count",
            inprogress_labels=True,
            should_group_status_codes=False,
        )

        instrumentator.add(app_up_metric())
        instrumentator.add(app_http_request_latency_seconds_metric())
        instrumentator.add(app_http_response_bytes_total_metric())
        instrumentator.add(app_http_response_error_count_metric())

        instrumentator.instrument(app)
        instrumentator.expose(app)
