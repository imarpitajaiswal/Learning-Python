try:
    from flask import Flask, render_template, request, redirect, url_for  # type: ignore[import]
except ImportError as e:
    raise ImportError("Flask is required to run this application. Install it with 'pip install flask'.") from e

import os
try:
    from PyPDF2 import PdfReader
except ImportError:
    try:
        import importlib
        PdfReader = importlib.import_module("pypdf").PdfReader
    except ImportError as e:
        raise ImportError("PyPDF2 or pypdf is required to run this application. Install it with 'pip install PyPDF2' or 'pip install pypdf'.") from e
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ----------------------------
# CONFIG
# ----------------------------
UPLOAD_FOLDER = "data/resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Sample job descriptions (you can expand this or load from DB/file)
JOB_DESCRIPTIONS = {
    "ML Engineer": "machine learning python tensorflow deep learning data science neural networks",
    "Data Analyst": "sql excel python data visualization pandas statistics business analysis",
    "Software Developer": "java python javascript web development backend frontend api databases"
}

# ----------------------------
# UTILITIES
# ----------------------------

def extract_text_from_pdf(file_path):
    """Extract text from uploaded PDF resume"""
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print("PDF extraction error:", e)
    return text.lower()


def clean_text(text):
    """Basic text cleaning"""
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower()


def extract_skills(text):
    """Simple skill extraction using keyword matching"""
    skills_db = [
        "python", "java", "sql", "machine learning", "deep learning",
        "tensorflow", "pandas", "numpy", "flask", "django",
        "javascript", "html", "css", "api", "git"
    ]

    found_skills = []
    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def calculate_ats_score(resume_text):
    """Simple ATS score based on keyword density & length"""
    keywords = ["python", "machine learning", "data", "project", "sql", "analysis"]

    score = 0
    for kw in keywords:
        if kw in resume_text:
            score += 10

    # normalize score to 100
    return min(score, 100)


def match_jobs(resume_text):
    """Match resume with job descriptions using TF-IDF similarity"""
    documents = [resume_text] + list(JOB_DESCRIPTIONS.values())

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    results = []
    for idx, job in enumerate(JOB_DESCRIPTIONS.keys()):
        results.append({
            "role": job,
            "match_score": round(similarity_scores[idx] * 100, 2)
        })

    # sort by best match
    results = sorted(results, key=lambda x: x["match_score"], reverse=True)

    return results


# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return redirect(url_for("home"))

    file = request.files["resume"]

    if file.filename == "":
        return redirect(url_for("home"))

    # Save file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract text
    resume_text = extract_text_from_pdf(file_path)
    resume_text = clean_text(resume_text)

    # AI Processing
    skills = extract_skills(resume_text)
    ats_score = calculate_ats_score(resume_text)
    job_matches = match_jobs(resume_text)

    return render_template(
        "results.html",
        skills=skills,
        ats_score=ats_score,
        job_matches=job_matches
    )


# ----------------------------
# MAIN
# ----------------------------

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
