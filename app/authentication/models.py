from tortoise import fields
from tortoise.models import Model

class User(Model):
    username = fields.CharField(pk=True, max_legth=50)
    hashed_password = fields.CharField(max_legth=50)
    mail = fields.CharField(max_legth=100)

    class Meta:
        table = "user" 