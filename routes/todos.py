from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

# http://localhost:8000/todos/
@router.get("/")
def get_todos_html(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("todos/merged_todo.html", context)