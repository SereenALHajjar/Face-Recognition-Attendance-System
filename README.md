# Face Recognition Attendance System

A modern web-based attendance system using FastAPI, SQLModel, and face recognition. Employees are registered with a photo, and attendance is marked by face recognition via webcam.

## Features
- Register employees with photo, name, email, position, salary, and password
- Secure login system with JWT authentication
- Role-based access control (admin/manager/employee)
- Mark attendance by face recognition (webcam capture)
- View all employees in a modern grid UI (admin/manager only)
- Delete and update employees from the UI (admin/manager only)
- Attendance statistics and averages (admin/manager only)
- RESTful API for CRUD operations
- Test suite for API endpoints

## Tech Stack
- **Backend:** FastAPI, SQLModel, SQLite, face_recognition
- **Frontend:** HTML, CSS, JavaScript 
- **Other:** Jinja2, OpenCV, Pillow

## Setup

### 1. Clone the repository
```sh
# Windows PowerShell
git clone https://github.com/SereenALHajjar/Face-Recognition-Attendance-System.git
cd FaceRecognitionAttendanceSystem
```

### 2. Create and activate a virtual environment
```sh
python -m venv .venv
.venv\Scripts\Activate
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the app
```sh
cd app
fastapi dev main.py
```

- The app will be available at: http://127.0.0.1:8000/

## Usage
- **Home page:** Capture your face to mark attendance.
- **Login:** Click "Login" to access admin/manager features.
- **Register:** Click "Register a New Employee" to add a new employee.
- **View All:** Click "View All Employees" (admin/manager only) to see all registered employees and delete them if needed.
- **Statistics:** Click "View Attendance Statistics" (admin/manager only) to see attendance stats and download CSV.

## API Endpoints

### Employee APIs
- `POST /employees/` - Register employee (multipart/form-data, returns Employee)
- `POST /employees/login` - Login and get JWT token (returns access_token)
- `GET /employees/all` - List all employees (admin/manager only)
- `GET /employees/{employee_id}` - Get employee by ID (returns Employee)
- `PUT /employees/{employee_id}` - Update employee (admin/manager only)
- `DELETE /employees/{employee_id}` - Delete employee (admin/manager only)
- `GET /employees/get-photo/{employee_id}` - Get employee photo (returns image file)

### Attendance APIs
- `GET /attendance/{employee_id}` - Mark attendance for employee (returns Attendance)

### Face Recognition
- `POST /face/compare` - Compare face and mark attendance (returns match info)

### Statistics APIs (admin/manager only)
- `GET /stats/attendance-summary` - Get summary stats for each employee (total days, absences, late entries)
- `GET /stats/attendance-averages` - Get average entry time, average departure time, and attendance rate for each employee

## Testing
Run all tests with:
```sh
pytest
```
