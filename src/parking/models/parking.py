from tortoise import fields, models


class Parking(models.Model):
    id = fields.IntField(pk=True)
    file = fields.CharField(max_length=255, unique=True)
    camera_id = fields.CharField(max_length=55, unique=True, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now_add=True)
