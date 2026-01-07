from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Union
from fastapi.templating import Jinja2Templates
from markupsafe import Markup
import json
from pydantic import BaseModel


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
templates.env.filters["tojson"] = lambda value: Markup(json.dumps(value, ensure_ascii=False))

@router.get("/welcome", response_class=HTMLResponse)
def welcome(auth : Union[str, None] = Query(default=None, min_lenght=11, max_lenght=15),
            id: Union[str, None] = Query(default=None, max_lenght=12)):
    return """<h2>Welcome Message!</h2>"""


@router.get("/text_message", response_class=HTMLResponse)
def text_message(auth : Union[str, None] = Query(default=None, min_lenght=11, max_lenght=15),
            id: Union[str, None] = Query(default=None, max_lenght=12)):
    return "<h2>Text Message</h2>"


@router.get("/control", response_class=HTMLResponse)
def text_message(auth : Union[str, None] = Query(default=None, min_lenght=11, max_lenght=15),
            id: Union[str, None] = Query(default=None, max_lenght=12)):
    return "<h2>TControl (Form)</h2>"


data = [
        {"id": 1, "Host": "홍길동", "VaultPath": 30},
        {"id": 2, "Host": "김철수", "VaultPath": 25},
        {"id": 3, "Host": "이영희", "VaultPath": 28},
        {"id": 4, "Host": "홍길동", "VaultPath": 30},
        {"id": 5, "Host": "김철수", "VaultPath": 25},
        {"id": 6, "Host": "이영희", "VaultPath": 28},
        {"id": 7, "Host": "홍길동", "VaultPath": 30},
        {"id": 8, "Host": "김철수", "VaultPath": 25},
        {"id": 9, "Host": "이영희", "VaultPath": 28},
        {"id": 10, "Host": "홍길동", "VaultPath": 30},
        {"id": 11, "Host": "김철수", "VaultPath": 25},
        {"id": 12, "Host": "이영희", "VaultPath": 28}
    ]

class DataItem(BaseModel):
    name: str
    age: int


@router.get("/tables", response_class=HTMLResponse)
def lists(request: Request,
        auth: Union[str, None] = Query(default=None, min_length=11, max_length=15),
        id: Union[str, None] = Query(default=None, max_length=12),
        ):
    title = "Table Lists"

    return templates.TemplateResponse("tables.html", {
        "request": request,
        "title": title,
        "data": data
    })


@router.post("/table_add")
async def add_data(item: DataItem):
    new_id = max([d["id"] for d in data], default=0) + 1
    new_item = {"id": new_id, "name": item.name, "age": item.age}
    data.append(new_item)
    return JSONResponse(content={"message": "성공", "item": new_item})


@router.get("/wizard", response_class=HTMLResponse)
def wizard():
    return "<h2>Wizard</h2>"


@router.get("/word_cloud", response_class=HTMLResponse)
def chart_pie():
    return "<h2>Word Cloud</h2>"


@router.get("/bar_plot", response_class=HTMLResponse)
def chart_bar():
    return "<h2>Bar Plot</h2>"


@router.get("/pie_plot", response_class=HTMLResponse)
def chart_pie():
    return "<h2>Pie Plot</h2>"


@router.get("/line_plot", response_class=HTMLResponse)
def chart_pie():
    return "<h2>Line Plot</h2>"


@router.get("/pie_plot", response_class=HTMLResponse)
def chart_pie():
    return "<h2>Pie Plot</h2>"


@router.get("/sankey_diagram", response_class=HTMLResponse)
def chart_pie():
    return "<h2>Sankey diagram</h2>"


@router.get("/collapsible_tree", response_class=HTMLResponse)
def chart_pie():
    return "<h2>Collapsible tree</h2>"


@router.get("/parallel", response_class=HTMLResponse)
def chart_pie():
    return "<h2>Parallel sets</h2>"


@router.get("/treemap", response_class=HTMLResponse)
def chart_pie():
    return "<h2>Treemap</h2>"


@router.get("/hierarchical", response_class=HTMLResponse)
def chart_pie():
    return "<h2>Hierarchical edge bundling</h2>"