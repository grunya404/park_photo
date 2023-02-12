import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware


def setup_sentry(app, settings):
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
        )

        app.add_middleware(SentryAsgiMiddleware)
