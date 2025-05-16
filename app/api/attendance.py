from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.db import get_session
import app.database.crud as db
from app.models.schemas import Employee

router = APIRouter(prefix="/attendance" , tags=["attendance"])

@router.get("/{employee_id}")
def update_attendance(employee_id: int , session: Session= Depends(get_session)):
    return db.update_attendance(session,employee_id) 
