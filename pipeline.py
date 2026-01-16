# pipeline.py

import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from utils import extract_text_from_pdf, clean_text, extract_skills_from_text
from skills import SKILL_LIST, LEARNING_TIME, MATCH_THRESHOLD, PARTIAL_THRESHOLD


# Load NLP model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(text1: str, text2: str) -> float:
    embeddings = model.encode([text1, text2])
    return float(
        cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    )


def analyze_skill_gap(resume_skills: list, job_skills: list):
    matched, partial, missing = [], [], []

    for job_skill in job_skills:
        best_score = 0
        best_match = None

        for resume_skill in resume_skills:
            score = semantic_similarity(resume_skill, job_skill)
            if score > best_score:
                best_score = score
                best_match = resume_skill

        if best_score >= MATCH_THRESHOLD:
            matched.append({
                "skill": job_skill,
                "matched_with": best_match,
                "similarity": round(best_score, 2)
            })
        elif best_score >= PARTIAL_THRESHOLD:
            partial.append({
                "skill": job_skill,
                "matched_with": best_match,
                "similarity": round(best_score, 2),
                "reason": "Basic or limited exposure"
            })
        else:
            missing.append(job_skill)

    return matched, partial, missing


def calculate_match_score(matched, partial, missing) -> float:
    total = len(matched) + len(partial) + len(missing)
    if total == 0:
        return 0.0
    score = (len(matched) + 0.5 * len(partial)) / total
    return round(score * 100, 2)


def estimate_learning_effort(partial, missing):
    effort = []

    for item in partial:
        skill = item["skill"]
        if skill in LEARNING_TIME:
            effort.append({
                "skill": skill,
                "time": LEARNING_TIME[skill]
            })

    for skill in missing:
        if skill in LEARNING_TIME:
            effort.append({
                "skill": skill,
                "time": LEARNING_TIME[skill]
            })

    return effort


def run_pipeline(resume_pdf_path: str, job_description: str) -> dict:
    resume_text = extract_text_from_pdf(resume_pdf_path)
    resume_clean = clean_text(resume_text)
    resume_skills = extract_skills_from_text(resume_clean, SKILL_LIST)

    job_clean = clean_text(job_description)
    job_skills = extract_skills_from_text(job_clean, SKILL_LIST)

    matched, partial, missing = analyze_skill_gap(resume_skills, job_skills)
    match_score = calculate_match_score(matched, partial, missing)
    learning_effort = estimate_learning_effort(partial, missing)

    recommendation = (
        "Strong fit" if match_score >= 75 else
        "Hireable with upskilling" if match_score >= 60 else
        "Not suitable for this role currently"
    )

    return {
        "overall_match_percent": match_score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "partial_skills": partial,
        "missing_skills": missing,
        "learning_effort": learning_effort,
        "recommendation": recommendation
    }


# Demo run
if __name__ == "__main__":
    job_description_text = """
    We are hiring a Backend Engineer with Python, REST APIs,
    Docker, Kubernetes, and cloud deployment experience.
    """

    result = run_pipeline("resume.pdf", job_description_text)
    print(json.dumps(result, indent=4))
