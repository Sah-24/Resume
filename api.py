from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv
import tempfile
import os

from pipeline import run_pipeline

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Resume Skill Match API")


def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@app.post("/match")
def match_resume(
    resume_path: str,
    job_description: str,
    x_api_key: str = Header(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        resume_path = tmp.name
        
    verify_api_key(x_api_key)
    
    os.remove(resume_path)
    result = run_pipeline(resume_path, job_description)
    return result

