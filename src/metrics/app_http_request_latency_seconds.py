from typing import Callable

from prometheus_client import Histogram
from prometheus_fastapi_instrumentator.metrics import Info


def app_http_request_latency_seconds_metric() -> Callable[[Info], None]:
    METRIC = Histogram(
        name="app_http_request_latency_seconds",
        documentation="Данная метрика содержит количество запросов в значении, разделенное на интервалы "
        "[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, +Inf]. "
        "Метка uri ДОЛЖНА содержать относительный URI для маршрута, для которого "
        "собирается метрика. Метка status_code ДОЛЖНА содержать код HTTP статуса запроса. "
        "Метка method ДОЛЖНА содержать название HTTP метода, который данный запрос исполнил. "
        "Примечание: обратите внимание, что в списке обязательных меток не содержится метка le, "
        "которая и так является обязательной для histogram типа метрики.",
        labelnames=("uri", "status_code", "method", "application"),
    )

    def instrumentation(info: Info) -> None:
        label_values = {
            "uri": info.modified_handler,
            "status_code": info.modified_status,
            "method": info.method,
            "application": info.application,
        }
        METRIC.labels(**label_values).observe(info.modified_duration)

    return instrumentation
