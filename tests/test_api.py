import os
from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import Employee


client = TestClient(app)



def test_create_employee():
    with open("ronaldo.jpg", "rb") as image_file:
        response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Ronaldo"
        assert response.json()["position"] == "tester"
        assert response.json()["email"] == "logintest@gmail.com"
        assert response.json()["salary"] == 4000
        
def test_get_employee_fail():
    response = client.get('/employees/99999')
    print(response.json())
    assert response.status_code == 404
    assert response.json()['detail'] == 'Employee not found.'
    
def test_get_employee_photo_pass():
    with open("ronaldo.jpg", "rb") as image_file:
        create_response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")}
        )
    assert create_response.status_code == 200
    emp_id = create_response.json()["id"]
    response = client.get(f"/employees/get-photo/{emp_id}")
    assert response.status_code == 200 or response.status_code == 404  

def test_get_employee_photo_fail():
    response = client.get('/employees/get-photo/99999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Employee not found.'


def test_delete_employee_pass():
    with open("ronaldo.jpg", "rb") as image_file:
        create_response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")}
        )
    assert create_response.status_code == 200
    emp_id = create_response.json()["id"]
    response = client.delete(f"/employees/{emp_id}")
    assert response.status_code == 204


def test_delete_employee_fail():
    response = client.delete('/employees/99999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Employee not found.'

def test_update_attendance():
    with open("ronaldo.jpg", "rb") as image_file:
        create_response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")}
        )
    assert create_response.status_code == 200
    emp_id = create_response.json()["id"]
    response = client.get(f"/attendance/{emp_id}")
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
    # Create an employee with a known face
    with open("ronaldo.jpg", "rb") as image_file:
        create_response = client.post(
            "/employees/",
            data={
                "name": "Ronaldo",
                "position": "tester",
                "email": "logintest@gmail.com",
                "salary": 4000
            },
            files={"photo": ("ronaldo.jpg", image_file, "image/jpeg")}
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
    assert data["match"] is True
    assert data["name"] == "Ronaldo"
    assert data["email"] == "logintest@gmail.com"
    assert data["position"] == "tester"
    assert data["salary"] == 4000


