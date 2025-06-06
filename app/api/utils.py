import json
import time
import cv2
import face_recognition
import numpy as np
from sqlmodel import Session, select
import app.database.crud as crud
import app.database.db as db
import app.models.schemas as schema

    
    
    
def load_file_and_encoding_face(file_path : str):
    img = face_recognition.load_image_file(file_path)
    return encoding_face(img)

def encoding_face(img):
    img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(img)
    if not encodings:
        return None  
    return encodings[0]

def compare_faces(cur_encoding):
    session = db.create_session() 
    employees = crud.return_all_employees(session) 
    session.close() 
    for emp in employees:
        if emp.encoding_face:
            stored_encoding = np.array(json.loads(emp.encoding_face))
            match = face_recognition.compare_faces([stored_encoding], cur_encoding)[0]
            if match:
                return {
                    'match': True,'emp':schema.Employee(
                    id= emp.id,
                    name= emp.name,
                    email= emp.email,
                    position= emp.position,
                    salary= emp.salary,
                    image_path= emp.image_path
                    )
                    
                }
    return {'match': False, 'message': 'Face not recognized. Please register.'}
