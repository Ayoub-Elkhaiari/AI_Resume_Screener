# app/utils.py
import os
from sentence_transformers import util
import pdfplumber
import docx
from app.models import model
from typing import Tuple

def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF or DOCX file.
    Raises ValueError for unsupported formats.
    """
    _, ext = os.path.splitext(file_path.lower())
    if ext == ".pdf":
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts).strip()
    elif ext == ".docx":
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs]).strip()
    else:
        raise ValueError("Unsupported file format. Supported: .pdf, .docx")

def compute_similarity(resume_text: str, job_description: str) -> float:
    """
    Compute cosine similarity between resume and job description.
    Returns float score in range [-1, 1], we expect 0..1 for semantic similarity.
    """
    if not resume_text:
        return 0.0
    if not job_description:
        return 0.0

    # use model from models.py - encodes strings to vectors
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    jd_emb     = model.encode(job_description, convert_to_tensor=True)
    score = util.cos_sim(resume_emb, jd_emb).item()
    # round for better presentation
    return round(float(score), 3)
