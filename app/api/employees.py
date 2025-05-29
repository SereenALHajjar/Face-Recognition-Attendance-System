import io
import json
import os
import shutil
import uuid
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, Body, status
from fastapi.responses import FileResponse
import numpy as np
from sqlmodel import Session
from app.api.utils import load_file_and_encoding_face
from app.database.db import get_session
import app.database.crud as db
from app.database.crud import EmployeeNotFoundError
from app.models.schemas import Employee
from PIL import Image
from pathlib import Path

router = APIRouter(prefix="/employees" , tags=["employees"])
UPLOAD_FOLDER = Path("uploads")


@router.get("/all", response_model=List[Employee])
def get_all_employees(session: Session = Depends(get_session)):
    return db.return_all_employees(session)

@router.get('/get-photo/{employee_id}', response_class=FileResponse)
def get_employee_photo(employee_id: int, session: Session = Depends(get_session)):
    try:
        employee = db.return_employee(session , employee_id)
    except EmployeeNotFoundError:
        raise HTTPException(status_code=404, detail="Employee not found.")
    file_path = Path(employee.image_path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(str(file_path))

@router.get("/{employee_id}", response_model=Employee)
def return_employee(employee_id : int, session:Session = Depends(get_session)): 
    try:
        return db.return_employee(session , employee_id)
    except EmployeeNotFoundError:
        raise HTTPException(status_code=404, detail="Employee not found.")

@router.post("/", response_model=Employee, status_code=status.HTTP_200_OK)
def create_employee(
    name: str = Form(...),
    email: str = Form(...),
    salary: float = Form(...),
    position: str = Form(...),
    photo: UploadFile = File(...), 
    session: Session = Depends(get_session)
):
    file_ext = Path(photo.filename).suffix
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_FOLDER / file_name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    encoding = load_file_and_encoding_face(str(file_path))
    employee = Employee(
        name=name,
        email=email,
        salary=salary,
        position=position,
        image_path=str(file_path), 
        encoding_face=json.dumps(encoding.tolist())
    )
    return db.create_employee(session , employee) 

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    try:
        db.delete_employee(session, employee_id)
        return Response(status_code=204)
    except EmployeeNotFoundError:
        raise HTTPException(status_code=404, detail="Employee not found.")

@router.put("/{employee_id}", response_model=Employee)
def update_employee_api(
    employee_id: int,
    update_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    try:
        updated_employee = db.update_employee(session, employee_id, update_data)
        return updated_employee
    except EmployeeNotFoundError:
        raise HTTPException(status_code=404, detail="Employee not found.")