import os
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from app.api import employees , attendance, face, stats
import app.database.db as db

app = FastAPI(    title="Face Recognition Attendance System",
    description="An AI-powered system to automate attendance tracking using face recognition technology.",
    version="1.0.0",
    contact={
        "name": "Sereen Al Hajjar",
        "url": "https://github.com/SereenALHajjar",
        "email": "sereen.alhajjar@gmail.com", 
    },
)
db.create_db_and_tables()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")
UPLOADS_DIR = os.path.join(BASE_DIR, "app", "uploads")
templates = Jinja2Templates(directory=STATIC_DIR)

app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(face.router)
app.include_router(stats.router)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

@app.get("/")
def serve_main(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})

@app.get("/add")
def serve_add_employess(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

@app.get("/employees-page")
def serve_employees_page(request: Request):
    return templates.TemplateResponse("employees.html", {"request": request})

@app.get("/stats-page")
def serve_stats_page(request: Request):
    return templates.TemplateResponse("stats.html", {"request": request})

@app.get("/login-page")
def serve_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})