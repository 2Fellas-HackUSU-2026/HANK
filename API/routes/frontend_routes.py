from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def read_index(request: Request):
    """
    Render the landing page template.

    Serves the main entry page for the application UI by returning
    `index.html` with the FastAPI `request` object in template context.

    Args:
        request: Current HTTP request injected by FastAPI.

    Returns:
        TemplateResponse: Rendered `index.html` response.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/actions")
def read_actions(request: Request):
    """
    Render the actions workflow page template.

    Serves the page used for action/hazard/control interaction by returning
    `actions.html` with the FastAPI `request` object in template context.

    Args:
        request: Current HTTP request injected by FastAPI.

    Returns:
        TemplateResponse: Rendered `actions.html` response.
    """
    return templates.TemplateResponse("actions.html", {"request": request})
