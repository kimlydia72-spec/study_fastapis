from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from urllib3 import request

app = FastAPI()

from routes.todos import router as todos_router
app.include_router(todos_router, prefix="/todos")

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

# 1. GET 방식: 쿼리 파라미터 읽기 (JSON 반환)
# http://localhost:8000/board/detail_json?title=Third%20Post&content=This%20is%20the%20third%20post.
@app.get("/board/detail_json")
async def board_detail_json(request: Request):
    # request.query_params는 딕셔너리처럼 동작합니다.
    params = request.query_params
    
    # params['title'] 대신 params.get('title')을 사용하면
    # 값이 없을 때 에러 대신 None을 반환하여 안전합니다.
    return {
        "title": params.get('title'), 
        "content": params.get('content')
    }

# http://localhost:8000/board/detail_json?title=Third%20Post&content=This%20is%20the%20third%20post.
# @app.get("/board/detail_json")
# async def board_detail_json(request: Request): # request = Request()
#     # request.method
#     # request.query_params
#     params = dict(request.query_params)

#     # return {"title": "Third Post", "content" : "This is the third post."}
#     return {"title": params['title'], "content": params['content']}

# 2. POST 방식: Form 데이터 읽기 (JSON 반환)
# HTML Form에서 action="/board/detail_post_json"으로 요청을 보낼 때 실행됨
@app.post("/board/detail_post_json")
async def board_detail_post_json(request: Request):
    # form 데이터는 비동기(async)로 읽어야 하므로 await가 필수입니다.
    form_data = await request.form()
    
    # 딕셔너리로 변환
    params = dict(form_data)

    return {
        "title": params.get('title'), 
        "content": params.get('content')
    }

# http://localhost:8000/board/detail_json?title=Third%20Post&content=This%20is%20the%20third%20post.
# @app.post("/board/detail_post_json")
# async def board_detail_post_json(request: Request): # request = Request()
#     # request.method
#     # request.query_params
#     params = dict(await request.form())

#     # return {"title": "Third Post", "content" : "This is the third post."}
#     return {"title": params['title'], "content": params['content']}

# 3. GET 방식: HTML 템플릿 렌더링
# http://localhost:8000/board/detail_html
@app.get("/board/detail_html", response_class=HTMLResponse)
async def main_html(request: Request):
    # [수정됨] "boards" -> "board" (폴더명 일치)
    return templates.TemplateResponse(
        "board/detail.html", 
        {"request": request}
    )

# http://localhost:8000/board/detail_html/{detail_id}
# @app.get("/board/detail_html/{detail_id}")
# async def main_html(request: Request, detail_id):
#     return templates.TemplateResponse("board/detail.html" 
#                                       , {"request": request})

# http://localhost:8000/board/detail_html
@app.get("/board/detail_html")
async def main_html(request: Request):
    return templates.TemplateResponse("board/detail.html" 
                                      , {"request": request})

# 정적 파일 설정
# from fastapi.staticfiles import StaticFiles
# app.mount("/images", StaticFiles(directory="resources/images"))
# app.mount("/css", StaticFiles(directory="resources/css"))

# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# import os

# app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "quests"))

# products = [
#     {"name": "Laptop", "price": 1200, "tags": ["electronics", "office"]},
#     {"name": "Smartphone", "price": 800, "tags": ["mobile", "electronics"]},
#     {"name": "Keyboard", "price": 100, "tags": ["accessories"]},
# ]

# @app.get("/products", response_class=HTMLResponse)
# async def products_page(request: Request):
#     return templates.TemplateResponse("10_jina2.html", {
#         "request": request,
#         "products": products
#     })

pass