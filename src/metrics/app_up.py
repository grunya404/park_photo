from typing import Callable

from prometheus_client import Gauge
from prometheus_fastapi_instrumentator.metrics import Info


def app_up_metric() -> Callable[[Info], None]:
    METRIC = Gauge(
        "app_up",
        "service",
        labelnames=("application",),
    )

    def instrumentation(info: Info) -> None:
        label_values = {"application": info.application}
        METRIC.labels(**label_values).set(1)

    return instrumentation
