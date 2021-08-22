from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import os
from starlette.staticfiles import StaticFiles

router = APIRouter()

path = os.path.dirname(__file__)
print(path)
templates = Jinja2Templates(path + "/../templates")

@router.get('/')
def home(request: Request):
    sentiments = [{"content": "This team looks very nice!", "description": "Arsenal form", "value": 1}]
    return templates.TemplateResponse('home.html', context={"request": request, "sentiments": sentiments})