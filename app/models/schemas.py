import datetime
from sqlmodel import SQLModel, Field
import datetime 
class Employee(SQLModel , table=True):
    id: int|None = Field(default=None , primary_key=True)
    name: str 
    salary : float 
    position : str 
    email : str 
    password: str
    image_path : str 
    encoding_face : str|None 
    
class Attendance(SQLModel , table = True):
    id: int|None = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    date: datetime.date
    entry_time: datetime.time|None = None
    departure_time: datetime.time|None = None