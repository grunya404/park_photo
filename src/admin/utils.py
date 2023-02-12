from enum import Enum
from typing import Any

from fastapi_admin.widgets.filters import Enum as FltEnum
from starlette.requests import Request


def str_to_bool(value: str) -> bool:
    if value.lower() in ["true", "yes", "1", "t", "y"]:
        return True
    return False


class YesNo(Enum):
    Yes = True
    No = False


class EnumFilter(FltEnum):
    async def parse_value(self, request: Request, value: Any):
        return self.enum_type(value)
