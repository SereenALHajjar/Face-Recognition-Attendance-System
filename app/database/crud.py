from sqlmodel import Session, select
from app.models.schemas import Employee , Attendance
from datetime import datetime

def create_employee(session: Session, employee: Employee):
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


def update_attendance(session: Session, employee_id: int):
    today = datetime.today().date()
    now = datetime.now().time()

    stmt = select(Attendance).where(
        Attendance.employee_id == employee_id,
        Attendance.date == today
    )
    attendance = session.exec(stmt).first()

    if not attendance:
        new_attendance = Attendance(
            employee_id=employee_id,
            date=today,
            entry_time=now
        )
        session.add(new_attendance)
        session.commit()
        session.refresh(new_attendance)
        return new_attendance
    elif not attendance.departure_time:
        attendance.departure_time = now
        session.add(attendance)
        session.commit()
        session.refresh(attendance)
        return attendance
    else:
        return attendance


def delete_employee(session: Session, employee_id: int):
    stmt = select(Employee).where(Employee.id == employee_id)
    result = session.exec(stmt).first()
    
    if not result:
        return {"error": "Employee not found."}
    
    session.delete(result)
    session.commit()
    return {"success": f"Employee with ID {employee_id} deleted."}


def return_employee(session: Session, employee_id: int):
    stmt = select(Employee).where(Employee.id == employee_id)
    result = session.exec(stmt).first()
    
    if not result:
        return {"error": "Employee not found."}
    return result
