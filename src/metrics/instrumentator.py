import os
from timeit import default_timer

from fastapi import FastAPI
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import metrics
from prometheus_fastapi_instrumentator.instrumentation import (
    PrometheusFastApiInstrumentator,
)
from starlette.requests import Request
from starlette.responses import Response


class FastApiInstrumentator(PrometheusFastApiInstrumentator):
    def instrument(self, app: FastAPI):
        if self.should_respect_env_var and os.environ.get(self.env_var_name, "false") != "true":
            return self

        if len(self.instrumentations) == 0:
            self.instrumentations.append(metrics.default())

        if self.should_instrument_requests_inprogress:
            labels = ("method", "uri", "application") if self.inprogress_labels else ()
            self.inprogress = Gauge(
                name=self.inprogress_name,
                documentation="Number of HTTP requests in progress.",
                labelnames=labels,
                multiprocess_mode="livesum",
            )

        # ----------------------------------------------------------------------

        @app.middleware("http")
        async def dispatch_middleware(request: Request, call_next) -> Response:
            start_time = default_timer()

            handler, is_templated = self._get_handler(request)
            is_excluded = self._is_handler_excluded(handler, is_templated)
            handler = "none" if not is_templated and self.should_group_untemplated else handler

            if not is_excluded and self.should_instrument_requests_inprogress:
                inprogress: Gauge
                if self.inprogress_labels:
                    inprogress = self.inprogress.labels(request.method, handler, app.title)
                else:
                    inprogress = self.inprogress
                inprogress.inc()

            response = None
            status = "500"

            try:
                response = await call_next(request)
                status = str(response.status_code)
            except Exception as e:
                raise e from None
            finally:
                if not is_excluded:
                    duration = max(default_timer() - start_time, 0)

                    if self.should_instrument_requests_inprogress:
                        inprogress.dec()  # type: ignore

                    if self.should_round_latency_decimals:
                        duration = round(duration, self.round_latency_decimals)

                    if self.should_group_status_codes:
                        status = status[0] + "xx"

                    info = metrics.Info(
                        request=request,
                        response=response,
                        method=request.method,
                        modified_handler=handler,
                        modified_status=status,
                        modified_duration=duration,
                    )
                    info.application = app.title

                    for instrumentation in self.instrumentations:
                        instrumentation(info)

            return response

        # ----------------------------------------------------------------------

        return self
