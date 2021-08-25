import os

from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from app.api.crud import get_all

router = APIRouter()

path = os.path.dirname(__file__)
templates = Jinja2Templates(path + "/../templates")


@router.get("/")
async def home(request: Request):
    all_sentiments = await get_all()
    sentiments = [
        {
            "content": sentiment["content"],
            "description": sentiment["description"],
            "sentiment": str(int(sentiment["sentiment"])),
        }
        for sentiment in all_sentiments
    ]
    return templates.TemplateResponse(
        "home.html", context={"request": request, "sentiments": sentiments}
    )
