from fastapi_admin.app import app
from fastapi_admin.resources import Link


@app.register
class Dashboard(Link):
    label = "Главная"
    icon = "fas fa-home"
    url = "/admin"
