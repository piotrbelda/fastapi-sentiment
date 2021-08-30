from typing import List

from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.api import crud
from app.models.pydantic import SentimentPayloadSchema, SentimentResponseSchema, SentimentUpdatePayloadSchema
from app.models.tortoise import SentimentSchema
from app.api.sentiment_predictor import predict_sentiment

router = APIRouter()


@router.post("/", response_model=SentimentResponseSchema, status_code=201)
async def create_sentiment(payload: SentimentPayloadSchema, background_tasks: BackgroundTasks) -> SentimentResponseSchema:
    
    sentiment_id = await crud.post(payload)
    
    background_tasks.add_task(predict_sentiment, sentiment_id, payload.content)
    
    response_object = {
        "id": sentiment_id,
        "content": payload.content,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=SentimentSchema)
async def read_sentiment(id: int) -> SentimentSchema:
    sentiment = await crud.get(id)
    if not sentiment:
        raise HTTPException(status_code=404, detail="Sentiment not found")
    return sentiment


@router.get("/", response_model=List[SentimentSchema])
async def read_all_sentiments() -> List[SentimentSchema]:
    return await crud.get_all()

@router.delete("/{id}/", response_model=SentimentResponseSchema)
async def delete_sentiment(id: int) -> SentimentResponseSchema:
    sentiment = await crud.get(id)
    if not sentiment:
        raise HTTPException(status_code=404, detail='Sentiment not found')
    await crud.delete(id)
    return sentiment

@router.put("/{id}/", response_model=SentimentSchema)
async def update_sentiment(id: int, payload: SentimentUpdatePayloadSchema) -> SentimentSchema:
    sentiment = await crud.put(id, payload)
    if not sentiment:
        raise HTTPException(status_code=404, detail="Sentiment not found")

    return sentiment