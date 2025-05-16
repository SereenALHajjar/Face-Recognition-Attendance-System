from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.db import get_session
import app.database.crud as db
from app.models.schemas import Employee

router = APIRouter(prefix="/employees" , tags=["employees"])

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    return db.delete_employee(session, employee_id)

@router.post("/")
def create_employee(employee:Employee, session: Session = Depends(get_session)):
    return db.create_employee(session , employee) 

@router.get("/{employee_id}")
def return_employee(employee_id : int, session:Session = Depends(get_session)): 
    return db.return_employee(session , employee_id)

