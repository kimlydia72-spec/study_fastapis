from fastapi import FastAPI

app = FastAPI()

# http://localhost:8000/
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# http://localhost:8000/html
@app.get("/html")
async def root_html():
    html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lydia</title>
        </head>
        <body>
            <div>My name is Lydia!</div>
        </body>
        </html>
        '''
    return html_content

from fastapi.templating import Jinja2Templates
from fastapi import Request
templates = Jinja2Templates(directory="templates/")

# http://localhost:8000/main_html
@app.get("/main_html")
async def main_html(request: Request):
    return templates.TemplateResponse("main.html", 
                                      {"request": request})

# http://localhost:8000/main_html_context
@app.get("/main_html_context")
async def main_html_context(request: Request):
    # 템플릿에 전달할 데이터
    context = {
        "request": request,
        "title": "FastAPI + Jinja Example",
        "items": ["Apple", "Banana", "Cherry"],
        "user": {"name": "Lydia", "age": 33}
    }
    return templates.TemplateResponse("main_context.html"
                                      , context)

# http://localhost:8000/users/list
@app.get("/users/list")
async def user_list(request: Request):
    users = [
    {"name": "Alice", "age": 25, "city": "Seoul"},
    {"name": "Bob", "age": 30, "city": "Busan"},
    {"name": "Charlie", "age": 28, "city": "Daegu"}
    ]

    context = {
        "request": request
        , "user_list": users
    }
    return templates.TemplateResponse("users/list.html"
                                      , context)

# http://localhost:8000/board/detail_json?title=Third%20Post&content=This%20is%20the%20third%20post.
@app.get("/board/detail_json")
async def board_detail_json(request: Request):
    return {"title": "Third Post", "content" : "This is the third post."}

# 정적 파일 설정
from fastapi.staticfiles import StaticFiles
app.mount("/images", StaticFiles(directory="resources/images"))
app.mount("/css", StaticFiles(directory="resources/css"))

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "quests"))

products = [
    {"name": "Laptop", "price": 1200, "tags": ["electronics", "office"]},
    {"name": "Smartphone", "price": 800, "tags": ["mobile", "electronics"]},
    {"name": "Keyboard", "price": 100, "tags": ["accessories"]},
]

@app.get("/products", response_class=HTMLResponse)
async def products_page(request: Request):
    return templates.TemplateResponse("10_jina2.html", {
        "request": request,
        "products": products
    })


pass 