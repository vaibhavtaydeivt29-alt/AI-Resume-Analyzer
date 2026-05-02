import streamlit as st
import re
from collections import Counter

# -------------------- CONFIG --------------------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# -------------------- SKILLS DATABASE --------------------
TECH_SKILLS = [
    "python", "sql", "mysql", "java", "c++", "javascript", "html", "css",
    "streamlit", "django", "flask", "react", "machine learning", "data analysis",
    "power bi", "excel", "git", "github", "oop", "api", "pandas", "numpy"
]

# -------------------- FUNCTIONS --------------------
def extract_text(uploaded_file):
    try:
        return uploaded_file.read().decode("utf-8")
    except:
        return "Could not read file. Upload a TXT file for now."


def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill in TECH_SKILLS:
        if skill in text:
            found_skills.append(skill)
    return found_skills


def calculate_score(skills):
    total_possible = len(TECH_SKILLS)
    score = (len(skills) / total_possible) * 100
    return round(score, 2)


def find_missing_skills(skills):
    return [skill for skill in TECH_SKILLS if skill not in skills]


def generate_feedback(score, missing_skills):
    feedback = []

    if score >= 70:
        feedback.append("Strong technical profile.")
    elif score >= 40:
        feedback.append("Good base, but can improve.")
    else:
        feedback.append("Resume needs stronger technical depth.")

    if missing_skills:
        feedback.append("Consider adding relevant projects using: " + ", ".join(missing_skills[:5]))

    return feedback


# -------------------- UI --------------------
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get ATS score, skills analysis, and suggestions.")

uploaded_file = st.file_uploader("Upload Resume (TXT file)", type=["txt"])

if uploaded_file:
    resume_text = extract_text(uploaded_file)

    st.subheader("Resume Content")
    st.text_area("Preview", resume_text, height=250)

    skills = extract_skills(resume_text)
    score = calculate_score(skills)
    missing_skills = find_missing_skills(skills)
    feedback = generate_feedback(score, missing_skills)

    st.subheader("ATS Score")
    st.progress(int(score))
    st.write(f"Score: {score}%")

    st.subheader("Detected Skills")
    if skills:
        for skill in skills:
            st.success(skill.title())
    else:
        st.warning("No technical skills detected")

    st.subheader("Missing Skills")
    if missing_skills:
        for skill in missing_skills[:10]:
            st.info(skill.title())

    st.subheader("Suggestions")
    for tip in feedback:
        st.write("✅", tip)

st.sidebar.title("How it works")
st.sidebar.write("1. Upload resume in TXT format")
st.sidebar.write("2. Skills are extracted")
st.sidebar.write("3. ATS score is calculated")
st.sidebar.write("4. Suggestions are generated")
