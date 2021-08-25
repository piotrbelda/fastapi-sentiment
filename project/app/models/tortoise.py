from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import DatetimeField, TextField
from tortoise.fields.data import BooleanField
from tortoise.models import Model


class TextSentiment(Model):
    content = TextField()
    description = TextField()
    sentiment = BooleanField()
    created_at = DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description


SentimentSchema = pydantic_model_creator(TextSentiment)
