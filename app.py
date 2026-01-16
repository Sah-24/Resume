import streamlit as st
import tempfile
import os

from pipeline import run_pipeline

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Resume Skill Matcher",
    page_icon="📄",
    layout="centered"
)

# -----------------------------
# UI HEADER
# -----------------------------
st.title("📄 Resume – Job Skill Matching")
st.caption("Explainable NLP-based resume screening")

st.divider()

# -----------------------------
# INPUTS
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=220,
    placeholder="Enter job requirements here..."
)

# -----------------------------
# RUN ANALYSIS
# -----------------------------
if st.button("Analyze Resume", use_container_width=True):

    if uploaded_file is None:
        st.warning("Please upload a resume PDF.")
        st.stop()

    if not job_description.strip():
        st.warning("Please paste a job description.")
        st.stop()

    # Save PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        resume_path = tmp.name

    with st.spinner("Analyzing resume..."):
        result = run_pipeline(resume_path, job_description)

    os.remove(resume_path)

    st.divider()

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.subheader("📊 Overall Match")
    st.metric(
        label="Match Percentage",
        value=f"{result['overall_match_percent']}%"
    )

    st.subheader("🧠 Recommendation")
    st.success(result["recommendation"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        if result["matched_skills"]:
            for skill in result["matched_skills"]:
                st.write(f"• {skill['skill']}")
        else:
            st.write("No strong matches")

    with col2:
        st.subheader("⚠️ Partial Skills")
        if result["partial_skills"]:
            for skill in result["partial_skills"]:
                st.write(f"• {skill['skill']}")
        else:
            st.write("None")

    st.subheader("❌ Missing Skills")
    if result["missing_skills"]:
        st.write(", ".join(result["missing_skills"]))
    else:
        st.write("None 🎉")

    st.subheader("📚 Learning Effort Estimation")
    if result["learning_effort"]:
        for item in result["learning_effort"]:
            st.write(f"• {item['skill']} → {item['time']}")
    else:
        st.write("No additional learning required")

    st.divider()
    st.caption("Model: Sentence-Transformers | Fully explainable pipeline")
