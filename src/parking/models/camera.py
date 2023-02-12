from tortoise import fields, models


class Camera(models.Model):
    id = fields.IntField(pk=True)
    camera_title_location = fields.CharField(max_length=255, unique=True)
    camera_url = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now_add=True)
