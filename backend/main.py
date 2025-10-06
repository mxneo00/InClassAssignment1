import os

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  # The URL where your React app is running
    # You can add other origins here, like production domains
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

templates = Jinja2Templates(directory="backend/public/html")
app.mount("/asset", StaticFiles(directory="backend/public/asset"), name="asset")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Landing", "host": "host"})
