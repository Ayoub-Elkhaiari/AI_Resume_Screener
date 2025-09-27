# app/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_screen_resume(monkeypatch):
    # Dummy CV content
    cv_content = b"My name is John Doe. I am a Python developer."

    # Mock extract_text to return CV text
    monkeypatch.setattr("app.utils.extract_text", lambda file_path: "My name is John Doe. I am a Python developer.")

    # Mock model.encode to return a tensor-like object
    class DummyTensor:
        def __init__(self, val):
            self.val = val
        def __sub__(self, other): return 0
        def __repr__(self): return "DummyTensor"
    # mock cosine similarity
    monkeypatch.setattr("app.utils.model", type("DummyModel", (), {"encode": lambda self, x, convert_to_tensor=True: DummyTensor(1)})())

    # Mock compute_similarity to return fixed score
    monkeypatch.setattr("app.utils.compute_similarity", lambda resume_text, jd_text: 0.85)

    files = {"file": ("dummy_cv.txt", BytesIO(cv_content), "text/plain")}
    data = {"job_description": "Looking for a Python developer"}

    response = client.post("/screen", files=files, data=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["similarity_score"] == 0.85
    assert json_data["file_name"] == "dummy_cv.txt"
