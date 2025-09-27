from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_screen_resume():
    # Dummy CV content
    cv_content = b"My name is John Doe. I am a Python developer."

    # FastAPI requires each file in files param: (parameter_name, (filename, fileobj, content_type))
    files = {
        "file": ("dummy_cv.txt", BytesIO(cv_content), "text/plain")
    }

    # Form fields must go in 'data'
    data = {
        "job_description": "Looking for a Python developer"
    }

    response = client.post("/screen", files=files, data=data)

    assert response.status_code == 200
    assert "similarity_score" in response.json()
