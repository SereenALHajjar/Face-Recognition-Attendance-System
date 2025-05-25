import face_recognition
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
import base64
import cv2
import PIL
import numpy as np
from sqlmodel import Session
from app.api.utils import compare_faces, encode_file , face_encoding
from io import BytesIO

from app.database.crud import update_attendance
from app.database.db import get_session

router = APIRouter(tags=["face"])

def load_image_file(file_bytes : bytes, mode='RGB'):

    file_data = BytesIO(file_bytes)

    im = PIL.Image.open(file_data)
    if mode:
        im = im.convert(mode)
    return np.array(im)


@router.post("/face/compare")
def compare_image(img: UploadFile = File(...) , session: Session = Depends(get_session)):
    array = load_image_file(img.file.read())
    # print("arra", array)
    encoding = encode_file(array)
    if encoding is None:
        return {"match": False, "message": "No face found in the image. Please try again with a clear face."}
    res = compare_faces(encoding) 
    if res.get("match"): 
        emp = res.get("emp")
        atten = update_attendance(session , emp.id)
        return {
                'match': True,
                'id': emp.id,
                'name': emp.name,
                'email': emp.email,
                'position': emp.position,
                'salary': emp.salary,
                'image_path': emp.image_path,
                'attendance': {
                    'date': str(atten.date) if atten and hasattr(atten, 'date') else None,
                    'entry_time': str(atten.entry_time) if atten and hasattr(atten, 'entry_time') else None,
                    'departure_time': str(atten.departure_time) if atten and hasattr(atten, 'departure_time') else None
                } if atten else None
        }
    return res
