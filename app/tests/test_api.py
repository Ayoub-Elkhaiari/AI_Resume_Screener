from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_screen_resume():
    # Prepare a dummy CV file
    cv_content = b"My name is John Doe. I am a Python developer."
    file_obj = BytesIO(cv_content)

    # files is a dict: key = parameter name in endpoint
    files = {"file": ("dummy_cv.txt", file_obj, "text/plain")}

    data = {"job_description": "Looking for a Python developer"}

    # POST request to /screen endpoint
    response = client.post("/screen", files=files, data=data)

    assert response.status_code == 200
    assert "similarity_score" in response.json()
