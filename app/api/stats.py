from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.db import get_session
import app.database.crud as db
from app.models.schemas import Employee, Attendance
from datetime import time, datetime, timedelta

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/attendance-summary")
def attendance_summary(session: Session = Depends(get_session)):
    employees = db.return_all_employees(session)
    stats = []
    for emp in employees:
        attendances = session.exec(
            db.Attendance.__table__.select().where(db.Attendance.employee_id == emp.id)
        ).all()
        total_days = len(attendances)
        absences = 0
        late_entries = 0
        for att in attendances:
            if att.entry_time and att.entry_time > time(9, 0):
                late_entries += 1
            if not att.entry_time:
                absences += 1
        stats.append({
            "employee_id": emp.id,
            "name": emp.name,
            "total_days": total_days,
            "absences": absences,
            "late_entries": late_entries
        })
    return stats

@router.get("/attendance-averages")
def attendance_averages(session: Session = Depends(get_session)):
    employees = db.return_all_employees(session)
    results = []
    for emp in employees:
        attendances = session.exec(
            db.Attendance.__table__.select().where(db.Attendance.employee_id == emp.id)
        ).all()
        entry_times = [att.entry_time for att in attendances if att.entry_time]
        departure_times = [att.departure_time for att in attendances if att.departure_time]
        total_days = len(attendances)
        # Calculate average entry time
        if entry_times:
            avg_entry_seconds = sum([t.hour*3600 + t.minute*60 + t.second for t in entry_times]) / len(entry_times)
            avg_entry = (datetime.min + timedelta(seconds=avg_entry_seconds)).time()
        else:
            avg_entry = None
        # Calculate average departure time
        if departure_times:
            avg_departure_seconds = sum([t.hour*3600 + t.minute*60 + t.second for t in departure_times]) / len(departure_times)
            avg_departure = (datetime.min + timedelta(seconds=avg_departure_seconds)).time()
        else:
            avg_departure = None
        # Attendance rate (days with entry_time / total days)
        attendance_days = len([att for att in attendances if att.entry_time])
        attendance_rate = (attendance_days / total_days) * 100 if total_days else 0
        results.append({
            "employee_id": emp.id,
            "name": emp.name,
            "average_entry_time": avg_entry.strftime('%H:%M:%S') if avg_entry else None,
            "average_departure_time": avg_departure.strftime('%H:%M:%S') if avg_departure else None,
            "attendance_rate": round(attendance_rate, 2)
        })
    return results
