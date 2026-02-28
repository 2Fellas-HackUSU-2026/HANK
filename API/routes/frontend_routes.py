from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/actions")
def read_actions(request: Request):
    return templates.TemplateResponse("actions.html", {"request": request})