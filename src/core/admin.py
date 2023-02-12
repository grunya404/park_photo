from fastapi_admin.app import app
from fastapi_admin.resources import Field, Model
from fastapi_admin.widgets import displays, filters, inputs

from admin.utils import EnumFilter, YesNo, str_to_bool

from .models import User


@app.register
class UserResource(Model):
    label = "Пользователи"
    model = User
    icon = "fas fa-user"
    page_pre_title = ""
    page_title = "Управление пользователями"
    filters = [
        filters.Search(name="username", label="Логин", search_mode="contains", placeholder=""),
        EnumFilter(name="is_active", label="Активный", null=True, enum=YesNo, enum_type=str_to_bool),
        filters.Enum(name="is_superuser", label="Админ", null=True, enum=YesNo, enum_type=str_to_bool),
    ]
    fields = [
        "id",
        Field(name="username", label="Логин"),
        Field(name="email", label="Email", input_=inputs.Email()),
        Field(name="is_active", label="Активный", input_=inputs.Switch(), display=displays.Boolean()),
        Field(name="is_superuser", label="Админ", input_=inputs.Switch(), display=displays.Boolean()),
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="created_at", label="Создан", display=displays.DatetimeDisplay(), input_=inputs.DisplayOnly()),
    ]
