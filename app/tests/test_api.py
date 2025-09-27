from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_screen_resume():
    # Prepare a dummy CV file
    from io import BytesIO
    cv_content = b"My name is John Doe. I am a Python developer."
    file = BytesIO(cv_content)
    file.name = "dummy_cv.txt"

    payload = {
        "job_description": "Looking for a Python developer",
        "file": file
    }

    response = client.post("/screen", files={"file": (file.name, file, "text/plain")}, data={"job_description": "Looking for a Python developer"})
    assert response.status_code == 200
    assert "similarity_score" in response.json()
