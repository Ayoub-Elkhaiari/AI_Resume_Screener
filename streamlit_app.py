# streamlit_app.py
import streamlit as st
import requests
import tempfile
import os

# backend URL used by the frontend; default to localhost, can be overridden with env var
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")  # compose service name
API_ENDPOINT = f"{BACKEND_URL}/screen"

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="centered")
st.title("📄 AI Resume Screener")
st.write("Upload a CV (PDF/DOCX) and paste a job description, or skip upload and paste both.")

uploaded_file = st.file_uploader("Upload your CV (PDF/DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Job description (paste or type here)", height=200)

col1, col2 = st.columns([1, 1])
with col1:
    btn_check = st.button("Check match")
with col2:
    st.write("")  # placeholder

if btn_check:
    if not job_description or not job_description.strip():
        st.warning("Please paste/enter a job description.")
    else:
        # If file uploaded -> send to backend, else send blank file with job_description
        try:
            if uploaded_file is not None:
                # Save to temp file so requests can use file path-like object
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    tmp_path = tmp.name
                files = {"file": open(tmp_path, "rb")}
            else:
                # create a tiny dummy text file when user didn't upload
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                    tmp.write(b"")
                    tmp_path = tmp.name
                files = {"file": open(tmp_path, "rb")}

            data = {"job_description": job_description}
            with st.spinner("Contacting backend and computing similarity..."):
                resp = requests.post(API_ENDPOINT, files=files, data=data, timeout=60)
            # close and remove temp file
            files["file"].close()
            try:
                os.remove(tmp_path)
            except Exception:
                pass

            if resp.status_code == 200:
                res = resp.json()
                score = res.get("similarity_score")
                st.subheader("Result")
                if score is not None:
                    if score > 0.5:
                        st.success(f"Match Score: {score} — Strong match ✅")
                    else:
                        st.error(f"Match Score: {score} — Weak match ⚠️")
                else:
                    st.info("No score returned.")
            else:
                st.error(f"Backend error: {resp.status_code} — {resp.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
