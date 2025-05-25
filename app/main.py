from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from app.api import employees , attendance, face
import app.database.db as db

app = FastAPI()
db.create_db_and_tables()


templates = Jinja2Templates(directory="static")

app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(face.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def serve_main(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})

@app.get("/add")
def serve_add_employess(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})