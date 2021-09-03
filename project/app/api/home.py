import os
from fastapi import APIRouter, Form, BackgroundTasks, status
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.api.sentiment_predictor import predict_sentiment
from app.api.crud import get_all, post
from app.models.pydantic import SentimentPayloadSchema
from app.api.sentiments import delete_sentiment
from typing import Optional

router = APIRouter()

path = os.path.dirname(__file__)
templates = Jinja2Templates(path + "/../templates")


@router.get("/")
async def home(request: Request):
    all_sentiments = await get_all()
    sentiments = [
        {
            "id": sentiment["id"],
            "content": '"' + sentiment["content"] + '"',
            "description": sentiment["description"],
            "sentiment": "positive" if sentiment["sentiment"] else "negative",
            "created_at": str(sentiment["created_at"]).split(".")[0]
        }
        for sentiment in all_sentiments
        ]
    return templates.TemplateResponse(
        "home.html", context={"request": request, "sentiments": sentiments})
        


@router.post("/")
async def submit_sentiment(request: Request, background_tasks: BackgroundTasks
                           , content: str = Form(...), description: str = Form(...)):
    
    payload = SentimentPayloadSchema(content=content, description=description)
    sentiment_id = await post(payload)
    
    background_tasks.add_task(predict_sentiment, sentiment_id, payload.content)
    
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{id}/")
async def delete_button(id: int):
    
    await delete_sentiment(id=id)
    
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)