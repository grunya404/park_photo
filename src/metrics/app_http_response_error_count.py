from typing import Callable

from prometheus_client import Counter
from prometheus_fastapi_instrumentator.metrics import Info


def app_http_response_error_count_metric() -> Callable[[Info], None]:
    METRIC = Counter(
        name="app_http_response_error_count",
        documentation="Количество ответов на запросы, с http статус кодом 5xx. "
        "Метка uri ДОЛЖНА содержать относительный URI для маршрута, "
        "для которого собирается метрика. Метка status_code ДОЛЖНА содержать код HTTP статуса запроса. "
        "Метка method ДОЛЖНА содержать название HTTP метода, который данный запрос исполнил.",
        labelnames=("uri", "status_code", "method", "application"),
    )

    def instrumentation(info: Info) -> None:
        if info.modified_status[0] == 5:
            label_values = {
                "uri": info.modified_handler,
                "status_code": info.modified_status,
                "method": info.method,
                "application": info.application,
            }
            METRIC.labels(**label_values).inc()

    return instrumentation
