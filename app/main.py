from fastapi import FastAPI
from app.api import employees , attendance
from app.database.db import create_db_and_tables

app = FastAPI()
create_db_and_tables()

app.include_router(employees.router)
app.include_router(attendance.router)

