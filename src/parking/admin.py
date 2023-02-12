from fastapi_admin.app import app
from fastapi_admin.resources import Field, Model
from fastapi_admin.widgets import displays, filters, inputs

from admin.utils import YesNo, str_to_bool, EnumFilter
from .models import Camera


@app.register
class CameraResource(Model):
    label = "Камеры"
    model = Camera
    icon = "ti ti-device-cctv"
    page_pre_title = ""
    page_title = "Управление камерами"
    filters = [
        filters.Search(name="camera_title_location", label="Расположение", search_mode="contains", placeholder="Парковка"),
        EnumFilter(name="is_active", label="Активный", null=True, enum=YesNo, enum_type=str_to_bool),
    ]
    fields = [
        "id",
        Field(name="camera_title_location", label="Расположение"),
        Field(name="camera_url", label="Адрес стрима"),
        Field(name="is_active", label="Активный", input_=inputs.Switch(), display=displays.Boolean()),
        Field(name="created_at", label="Создан", display=displays.DatetimeDisplay(), input_=inputs.DisplayOnly()),
    ]
