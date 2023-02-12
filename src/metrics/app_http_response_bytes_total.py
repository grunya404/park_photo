from typing import Callable

from prometheus_client import Counter
from prometheus_fastapi_instrumentator.metrics import Info


def app_http_response_bytes_total_metric() -> Callable[[Info], None]:
    METRIC = Counter(
        name="app_http_response_bytes_total",
        documentation="Данная метрика ДОЛЖНА содержать счетчик количества байт контента, которое вернул сервис в ответах "
        "на запросы. В разрезе следующих меток. Метка uri ДОЛЖНА содержать относительный URI для маршрута, "
        "для которого собирается метрика. Метка status_code ДОЛЖНА содержать код HTTP статуса запроса. "
        "Метка method ДОЛЖНА содержать название HTTP метода, который данный запрос исполнил.",
        labelnames=("uri", "status_code", "method", "application"),
    )

    def instrumentation(info: Info) -> None:
        if info.response and hasattr(info.response, "headers"):
            content_length = info.response.headers.get("Content-Length", 0)
        else:
            content_length = 0

        label_values = {
            "uri": info.modified_handler,
            "status_code": info.modified_status,
            "method": info.method,
            "application": info.application,
        }

        METRIC.labels(**label_values).inc(int(content_length))

    return instrumentation
