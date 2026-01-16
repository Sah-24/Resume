# utils.py

import pdfplumber
import re


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.# ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skills_from_text(text: str, skill_list: list) -> list:
    found = set()
    for skill in skill_list:
        if skill in text:
            found.add(skill)
    return list(found)
