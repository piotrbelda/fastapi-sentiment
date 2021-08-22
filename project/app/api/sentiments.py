from fastapi import APIRouter, HTTPException
from app.api import crud
from app.models.pydantic import SentimentPayloadSchema, SentimentResponseSchema
from app.models.tortoise import SentimentSchema
from typing import List

router = APIRouter()

@router.post("/", response_model=SentimentResponseSchema, status_code=201)
async def create_sentiment(payload: SentimentPayloadSchema) -> SentimentResponseSchema:
    sentiment_id = await crud.post(payload)
    response_object = {
        "id": sentiment_id,
        "content": payload.content,
        "description": payload.description
    }
    return response_object

@router.get("/{id}/", response_model=SentimentSchema)
async def read_sentiment(id: int) -> SentimentSchema:
    sentiment = await crud.get(id)
    if not sentiment:
        raise HTTPException(status_code=404, detail="Summary not found")
    return sentiment

@router.get("/", response_model=List[SentimentSchema])
async def read_all_summaries() -> List[SentimentSchema]:
    return await crud.get_all()