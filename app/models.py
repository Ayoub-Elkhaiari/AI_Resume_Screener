# app/models.py
from sentence_transformers import SentenceTransformer

# Load model once at process start to avoid reloading on each request
# use a small model that's fast and effective
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)
