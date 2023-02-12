import importlib
import os

from babel.support import Translations
from fastapi_admin.app import app as admin_app
from fastapi_admin.i18n import TRANSLATIONS

from core.models.user import User
from redis.session import redis
from .login import UsernamePasswordProvider

login_provider = UsernamePasswordProvider(admin_model=User,
                                          login_logo_url="https://preview.tabler.io/static/logo.svg")


def load_admin(settings):
    for module in settings.MODULES:
        module_admin = f"{module}/admin.py"
        if os.path.isfile(module_admin):
            importlib.import_module(module_admin[:-3].replace("/", "."))


async def setup_admin(app, settings):
    TRANSLATIONS["ru"] = Translations.load(os.path.join(settings.BASE_DIR,
                                                        "admin", "locales"), locales=["ru_RU"])
    load_admin(settings)
    if settings.ENVIRONMENT != 'local':
        admin_path = f"/{settings.SERVICE_NAME}{settings.ADMIN_PATH}"
    else:
        admin_path = settings.ADMIN_PATH

    await admin_app.configure(
        template_folders=[os.path.join(settings.BASE_DIR, "admin", "templates")],
        logo_url=f"{settings.STATIC_URL}admin/logo-white.svg",
        favicon_url=f"{settings.STATIC_URL}admin/favicon.ico",
        language_switch=False,
        default_locale="ru",
        providers=[login_provider],
        redis=redis,
        admin_path=admin_path,
    )
    app.mount(settings.ADMIN_PATH, admin_app)
