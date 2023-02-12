import asyncio
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tortoise import Tortoise

from config import settings
from parking.tasks import get_screenshots, get_free_places


async def task_create_screens():
    await Tortoise.init(
        config=settings.TORTOISE_CONFIG)
    await get_screenshots()


async def task_free_places():
    await Tortoise.init(
        config=settings.TORTOISE_CONFIG)
    await get_free_places()


def run():
    scheduler = AsyncIOScheduler()

    logging.getLogger('apscheduler.executors.default').setLevel(logging.ERROR)
    if settings.SENTRY_DSN:
        import sentry_sdk

        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,

        )

    scheduler.add_job(task_create_screens, "interval", minutes=settings.PERIODIC_GET_SCREENSHOT_MINUTE)
    scheduler.add_job(task_free_places, "interval", minutes=settings.PERIODIC_GET_FREE_PLACE_MINUTE)

    scheduler.start()
    print("Press Ctrl+{0} to exit".format("Break" if os.name == "nt" else "C"))

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    run()
