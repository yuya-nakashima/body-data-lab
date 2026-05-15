from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/reflections", response_class=HTMLResponse)
def reflections_ui(request: Request):
    return templates.TemplateResponse(request, "reflections.html")


@router.get("/reflections/list", response_class=HTMLResponse)
def reflections_list_ui(request: Request):
    return templates.TemplateResponse(request, "reflections_list.html")


@router.get("/habits", response_class=HTMLResponse)
def habits_ui(request: Request):
    return templates.TemplateResponse(request, "habits.html")


@router.get("/wishes", response_class=HTMLResponse)
def wishes_ui(request: Request):
    return templates.TemplateResponse(request, "wishes.html")


@router.get("/daily-goals", response_class=HTMLResponse)
def daily_goals_ui(request: Request):
    return templates.TemplateResponse(request, "daily_goals.html")


@router.get("/steps", response_class=HTMLResponse)
def steps_ui(request: Request):
    return templates.TemplateResponse(request, "steps.html")
