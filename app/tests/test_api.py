from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_similarity():
    payload = {"cv_text": "Python developer", "job_text": "Looking for Python skills"}
    response = client.post("/similarity", json=payload)
    assert response.status_code == 200
    assert "similarity" in response.json()

def test_score():
    payload = {"cv_text": "Machine learning engineer", "job_text": "AI engineer with ML experience"}
    response = client.post("/score", json=payload)
    assert response.status_code == 200
    assert "score" in response.json()
