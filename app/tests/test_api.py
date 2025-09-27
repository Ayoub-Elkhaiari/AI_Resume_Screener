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
    
    # Create a fresh BytesIO object for each request
    file_obj = BytesIO(cv_content)
    
    # FastAPI expects a tuple: (filename, fileobj, content_type)
    files = {
        "file": ("dummy_cv.txt", file_obj, "text/plain")
    }
    
    # Form field
    data = {
        "job_description": "Looking for a Python developer"
    }
    
    response = client.post("/screen", files=files, data=data)
    
    # Assert successful response
    assert response.status_code == 200
    assert "similarity_score" in response.json()
