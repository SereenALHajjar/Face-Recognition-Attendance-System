import face_recognition
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
import base64
import cv2
import PIL
import numpy as np
from sqlmodel import Session
from app.api.utils import compare_faces, encoding_face, load_file_and_encoding_face
from io import BytesIO

from app.database.crud import update_attendance
from app.database.db import get_session

router = APIRouter(tags=["face"])

class AttendanceInfo(BaseModel):
    date: str = None
    entry_time: str = None
    departure_time: str = None

class CompareImageResponse(BaseModel):
    match: bool
    id: int = None
    name: str = None
    email: str = None
    position: str = None
    salary: float = None
    image_path: str = None
    attendance: AttendanceInfo = None
    message: str = None

def load_image_file(file_bytes: bytes, mode='RGB'):

    file_data = BytesIO(file_bytes)

    im = PIL.Image.open(file_data)
    if mode:
        im = im.convert(mode)
    return np.array(im)

@router.post("/face/compare" , response_model=CompareImageResponse)
def compare_image(img: UploadFile = File(...) , session: Session = Depends(get_session)):
    array = load_image_file(img.file.read())
    encoding = encoding_face(array)
    if encoding is None:
        raise HTTPException(status_code=400, detail="No face found in the image. Please try again with a clear face.")
    res = compare_faces(encoding) 
    if res.get("match"): 
        employee = res.get("emp")
        employee_attendance = update_attendance(session , employee.id)
        attendance_info = None
        if employee_attendance:
            attendance_info = AttendanceInfo(
                date=str(employee_attendance.date) if hasattr(employee_attendance, 'date') else None,
                entry_time=str(employee_attendance.entry_time) if hasattr(employee_attendance, 'entry_time') else None,
                departure_time=str(employee_attendance.departure_time) if hasattr(employee_attendance, 'departure_time') else None
            )
        return CompareImageResponse(
            match=True,
            id=employee.id,
            name=employee.name,
            email=employee.email,
            position=employee.position,
            salary=employee.salary,
            image_path=employee.image_path,
            attendance=attendance_info
        )
    raise HTTPException(status_code=404, detail=res.get("message"))
