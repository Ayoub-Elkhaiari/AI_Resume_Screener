# app/main.py
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from app.utils import extract_text, compute_similarity

app = FastAPI(title="AI Resume Screener API")

# Allow requests from Streamlit frontend (set broader for demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "AI Resume Screener backend is running"}

@app.post("/screen")
async def screen_resume(file: UploadFile, job_description: str = Form(...)):
    # Validate
    if not job_description or not job_description.strip():
        raise HTTPException(status_code=400, detail="job_description empty")
    if not file:
        raise HTTPException(status_code=400, detail="file missing")

    # Save uploaded file to temp file (keeping extension)
    suffix = os.path.splitext(file.filename)[1] or ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # extract text and compute similarity
        resume_text = extract_text(tmp_path)
        score = compute_similarity(resume_text, job_description)

        return {"similarity_score": score, "file_name": file.filename}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # cleanup
        try:
            os.remove(tmp_path)
        except Exception:
            pass
