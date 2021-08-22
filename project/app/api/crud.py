from typing import Text
from app.models.pydantic import SentimentPayloadSchema
from app.models.tortoise import TextSentiment
from typing import Union, List

async def post(payload: SentimentPayloadSchema) -> int:
    sentiment = TextSentiment(
        content = payload.content,
        description = payload.description,
        sentiment = True
    )
    await sentiment.save()
    return sentiment.id

async def get(id: int) -> Union[dict, None]:
    sentiment = await TextSentiment.filter(id=id).first().values()
    if sentiment:
        return sentiment[0]
    return None

async def get_all() -> List:
    summaries = await TextSentiment.all().values()
    return summaries