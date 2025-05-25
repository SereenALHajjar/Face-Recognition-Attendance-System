import io
import json
import os
import shutil
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
import numpy as np
from sqlmodel import Session
from app.api.utils import face_encoding
from app.database.db import get_session
import app.database.crud as db
from app.models.schemas import Employee
from PIL import Image

router = APIRouter(prefix="/employees" , tags=["employees"])
UPLOAD_FOLDER = "uploads"

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    return db.delete_employee(session, employee_id)

@router.post("/")
def create_employee(name: str = Form(...),
    email: str = Form(...),
    salary: float = Form(...),
    position: str = Form(...),
    photo: UploadFile = File(...), 
    session: Session = Depends(get_session)):
    
    file_ext = os.path.splitext(photo.filename)[1]
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
        
    encoding = face_encoding(file_path)
    print(encoding)
    employee = Employee(
        name=name,
        email=email,
        salary=salary,
        position=position,
        image_path=file_path.replace("\\", "/"), 
        encoding_face=json.dumps(encoding.tolist())
    )
    return db.create_employee(session , employee) 

@router.get("/{employee_id}")
def return_employee(employee_id : int, session:Session = Depends(get_session)): 
    return db.return_employee(session , employee_id)

@router.get('/get-photo/{employee_id}')
def get_employee_photo(employee_id: int, session: Session = Depends(get_session)):
    employee = db.return_employee(session , employee_id)
    file_path =  employee.image_path


    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # Return the image file as a response
    return FileResponse(file_path)