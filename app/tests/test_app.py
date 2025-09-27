# tests/test_utils.py
from app.utils import compute_similarity

def test_similarity_related():
    score = compute_similarity(
        "Experienced Python developer with machine learning background and PyTorch experience.",
        "Looking for a Python Machine Learning engineer experienced in PyTorch and ML."
    )
    assert score > 0.4  # model dependent; choose a modest threshold

def test_similarity_unrelated():
    score = compute_similarity(
        "Pastry chef with 10 years experience making croissants and cakes.",
        "Senior backend engineer required with Python, Docker and AWS experience."
    )
    assert score < 0.3
