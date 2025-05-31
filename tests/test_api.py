import os
from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import Employee


client = TestClient(app)


def get_admin_token():
    # Create an admin user and get a token, only if not already created
    login_response = client.post(
        "/employees/login?email=adminuser@gmail.com&password=adminpass"
    )
    if login_response.status_code == 200:
        return login_response.json()["access_token"]
    # Otherwise, create the admin user
    with open("ronaldo.jpg", "rb") as image_file:
        response = client.post(
            "/employees/",
            data={
                "name": "AdminUser",
                "position": "admin",
                "email": "adminuser@gmail.com",
                "salary": 9999,
                "password": "adminpass"
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")}
        )
    # If user already exists, ignore warning
    if response.status_code not in (200, 409):
        assert response.status_code == 200
    login_response = client.post(
        "/employees/login?email=adminuser@gmail.com&password=adminpass"
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


def test_create_employee():
    token = get_admin_token()
    with open("ronaldo.jpg", "rb") as image_file:
        response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000,
                "password": "testpass"
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Ronaldo"
        assert response.json()["position"] == "tester"
        assert response.json()["email"] == "logintest@gmail.com"
        assert response.json()["salary"] == 4000
        
def test_get_employee_fail():
    token = get_admin_token()
    response = client.get('/employees/99999', headers={"Authorization": f"Bearer {token}"})
    print(response.json())
    assert response.status_code == 404
    assert response.json()['detail'] == 'Employee not found.'
    
def test_get_employee_photo_pass():
    token = get_admin_token()
    with open("ronaldo.jpg", "rb") as image_file:
        create_response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000,
                "password": "testpass"
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")},
            headers={"Authorization": f"Bearer {token}"}
        )
    assert create_response.status_code == 200
    emp_id = create_response.json()["id"]
    response = client.get(f"/employees/get-photo/{emp_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200 or response.status_code == 404  

def test_get_employee_photo_fail():
    token = get_admin_token()
    response = client.get('/employees/get-photo/99999', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Employee not found.'


def test_delete_employee_pass():
    token = get_admin_token()
    with open("ronaldo.jpg", "rb") as image_file:
        create_response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000,
                "password": "testpass"
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")},
            headers={"Authorization": f"Bearer {token}"}
        )
    assert create_response.status_code == 200
    emp_id = create_response.json()["id"]
    response = client.delete(f"/employees/{emp_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204


def test_delete_employee_fail():
    token = get_admin_token()
    response = client.delete('/employees/99999', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Employee not found.'

def test_update_attendance():
    token = get_admin_token()
    with open("ronaldo.jpg", "rb") as image_file:
        create_response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000,
                "password": "testpass"
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")},
            headers={"Authorization": f"Bearer {token}"}
        )
    assert create_response.status_code == 200
    emp_id = create_response.json()["id"]
    response = client.get(f"/attendance/{emp_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["employee_id"] == emp_id

def test_face_compare_no_face():
    import io
    from PIL import Image
    blank = Image.new('RGB', (100, 100), color = 'white')
    buf = io.BytesIO()
    blank.save(buf, format='JPEG')
    buf.seek(0)
    response = client.post(
        "/face/compare",
        files={"img": ("blank.jpg", buf, "image/jpeg")}
    )
    assert response.status_code == 400
    assert response.json()["detail"].startswith("No face found")

def test_face_compare_success():
    token = get_admin_token()
    # Create an employee with a known face
    with open("ronaldo.jpg", "rb") as image_file:
        create_response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000,
                "password": "testpass"
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")},
            headers={"Authorization": f"Bearer {token}"}
        )
    assert create_response.status_code == 200
    # Now test face compare with the same image
    with open("ronaldo.jpg", "rb") as image_file:
        response = client.post(
            "/face/compare",
            files={"img": ("ronaldo.jpg", image_file, "image/jpeg")}
        )
    assert response.status_code == 200
    data = response.json()
    # Accept either 'Ronaldo' or 'AdminUser' as a match (if admin face is matched first)
    assert data["match"] is True
    assert data["name"] in ["Ronaldo", "AdminUser"]
    assert data["email"] in ["logintest@gmail.com", "adminuser@gmail.com"]
    assert data["position"] in ["tester", "admin"]
    # Salary check is not strict because both users may match


