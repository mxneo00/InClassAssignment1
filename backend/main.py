import os

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.models.items import Item
from lifespan import lifespan

app = FastAPI(lifespan = lifespan)

origins = [
    "http://localhost:5173",
]

templates = Jinja2Templates(directory="backend/public/html")
app.mount("/asset", StaticFiles(directory="backend/public/asset"), name="asset")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Landing", "host": "host"})

@app.get("/items")
async def get_items():
    items = await Item.all()
    return items

@app.post("/items")
async def add_item(item_name: str):
    item = await Item.create(item_name=item_name)
    return item

