from typing import List, Text, Union

from app.models.pydantic import SentimentPayloadSchema
from app.models.tortoise import TextSentiment


async def post(payload: SentimentPayloadSchema) -> int:
    sentiment = TextSentiment(
        content=payload.content, description=payload.description, sentiment=True
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

async def delete(id: int) -> int:
    sentiment = await TextSentiment.filter(id=id).first().delete()
    return sentiment

async def put(id: int, payload: SentimentPayloadSchema) -> Union[dict, None]:
    sentiment = await TextSentiment.filter(id=id).update(content=payload.content, description=payload.description, sentiment=payload.sentiment)
    if sentiment:
        updated_sentiment = await TextSentiment.filter(id=id).first().values()
        return updated_sentiment[0]
    return None
