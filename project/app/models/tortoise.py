from tortoise import fields
from tortoise.models import Model
from tortoise.fields.data import BooleanField
from tortoise.fields import TextField, DatetimeField

class TextSentiment(Model):
    content = TextField()
    description = TextField()
    sentiment = BooleanField()
    created_at = DatetimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.description