# Resume Skill Matching System

An explainable NLP-based system that matches resumes against job descriptions,
identifies skill gaps, and provides learning recommendations.

Built for hackathon use with clean ML logic, API access, and Streamlit UI.

---

## 🚀 Features

- Resume PDF parsing
- Job description analysis
- Skill extraction
- Semantic skill matching (Transformer-based)
- Explainable match score
- Skill gap analysis (Matched / Partial / Missing)
- Learning effort estimation
- Streamlit demo UI
- FastAPI backend support

---

## 🧠 Tech Stack

- Python 3.9+
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Scikit-learn
- PDFPlumber
- FastAPI (API layer)
- Streamlit (UI)

---

## 📁 Project Structure
resume-skill-matcher/
├── app.py # Streamlit UI
├── api.py # FastAPI backend
├── pipeline.py # Core ML pipeline
├── utils.py # Text & PDF utilities
├── skills.py # Skill config & thresholds
├── requirements.txt
├── README.md
└── .gitignore
