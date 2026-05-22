"""
Resume Analyzer Application
A Flask-based web application for analyzing resumes, extracting skills,
calculating ATS scores, and matching resumes with job descriptions.
"""

import os
import re
import logging
import tempfile
from datetime import datetime
from pathlib import Path

try:
    from flask import Flask, render_template, request, redirect, url_for, flash
except ImportError as e:
    raise ImportError(
        "Flask is required to run this application. Install it with 'pip install flask'."
    ) from e

try:
    from PyPDF2 import PdfReader
except ImportError:
    try:
        import importlib
        PdfReader = importlib.import_module("pypdf").PdfReader
    except ImportError as e:
        raise ImportError(
            "PyPDF2 or pypdf is required to run this application. "
            "Install it with 'pip install PyPDF2' or 'pip install pypdf'."
        ) from e

from werkzeug.utils import secure_filename
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# LOGGING SETUP
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ----------------------------
# FLASK APP INITIALIZATION
# ----------------------------
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# ----------------------------
# CONFIGURATION
# ----------------------------

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'resumes')
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_FILENAME_LENGTH = 255

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ATS Score configuration
ATS_KEYWORDS = {
    "python": 15,
    "machine learning": 20,
    "data": 10,
    "project": 8,
    "sql": 15,
    "analysis": 10,
    "experience": 8,
    "skills": 8,
    "java": 15,
    "javascript": 12,
    "cloud": 12,
    "aws": 15,
    "docker": 12,
    "api": 10,
    "git": 10
}

# Job descriptions database (expandable)
JOB_DESCRIPTIONS = {
    "ML Engineer": (
        "machine learning python tensorflow deep learning data science neural networks "
        "pytorch scikit-learn model training data preprocessing algorithm optimization"
    ),
    "Data Analyst": (
        "sql excel python data visualization pandas statistics business analysis "
        "tableau power bi data warehousing etl reporting insights"
    ),
    "Software Developer": (
        "java python javascript web development backend frontend api databases "
        "rest microservices testing cloud deployment ci/cd"
    ),
    "Data Scientist": (
        "python r data science machine learning statistics sql visualization "
        "big data hadoop spark deep learning analytics"
    ),
    "DevOps Engineer": (
        "docker kubernetes cloud aws azure ci cd jenkins terraform infrastructure "
        "monitoring logging automation deployment"
    )
}

# Skills database (comprehensive)
SKILLS_DB = {
    # Programming Languages
    "python", "java", "javascript", "c++", "c#", "php", "ruby", "go", "rust", "swift",
    "kotlin", "typescript", "scala", "r", "matlab", "sql", "shell", "bash",
    
    # Web Technologies
    "html", "css", "react", "vue", "angular", "node.js", "express", "django",
    "flask", "spring", "fastapi", "web development", "rest", "graphql", "websocket",
    
    # Data & AI/ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "keras", "scikit-learn",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly", "data analysis", "big data",
    "spark", "hadoop", "nlp", "computer vision", "reinforcement learning",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "oracle",
    "cassandra", "dynamodb", "firebase", "database design",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "gitlab", "github",
    "terraform", "ansible", "ci/cd", "devops", "cloud computing", "aws lambda",
    "apache", "nginx", "linux",
    
    # Other Technologies
    "git", "api", "microservices", "testing", "jira", "agile", "scrum",
    "problem solving", "communication", "leadership", "teamwork"
}

# ----------------------------
# UTILITY FUNCTIONS
# ----------------------------

def allowed_file(filename):
    """Check if file extension is allowed"""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def validate_filename(filename):
    """Validate and sanitize filename"""
    if len(filename) > MAX_FILENAME_LENGTH:
        filename = filename[:MAX_FILENAME_LENGTH]
    return secure_filename(filename)


def extract_text_from_pdf(file_path):
    """
    Extract text from uploaded PDF resume
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted and lowercased text from the PDF
        
    Raises:
        ValueError: If PDF extraction fails or returns empty text
    """
    text = ""
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"Resume file not found: {file_path}")
            
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            
            if not reader.pages:
                logger.warning(f"PDF has no pages: {file_path}")
                raise ValueError("PDF file is empty or corrupted")
            
            for page_num, page in enumerate(reader.pages):
                try:
                    extracted_text = page.extract_text() or ""
                    text += extracted_text + " "
                except Exception as page_error:
                    logger.warning(f"Error extracting page {page_num}: {page_error}")
                    continue
                    
        if not text.strip():
            logger.warning(f"No text extracted from PDF: {file_path}")
            raise ValueError("Could not extract text from PDF. File may be corrupted or image-only.")
            
        logger.info(f"Successfully extracted {len(text)} characters from {file_path}")
        return text.lower().strip()
        
    except FileNotFoundError as e:
        logger.error(f"PDF file not found: {e}")
        raise
    except ValueError as e:
        logger.error(f"PDF processing error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected PDF extraction error: {e}")
        raise ValueError(f"PDF extraction failed: {str(e)}")


def clean_text(text):
    """
    Clean and normalize text
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove special characters, keep only letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.lower().strip()


def extract_skills(text):
    """
    Extract skills from text using keyword matching
    
    Args:
        text (str): Resume text
        
    Returns:
        list: List of found skills (deduplicated and sorted)
    """
    if not text:
        return []
    
    found_skills = set()  # Using set for O(1) lookup and deduplication
    
    for skill in SKILLS_DB:
        # Use word boundaries for better matching
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.add(skill.title())
    
    return sorted(list(found_skills))


def calculate_ats_score(resume_text):
    """
    Calculate ATS (Applicant Tracking System) score based on keyword density
    
    Args:
        resume_text (str): Cleaned resume text
        
    Returns:
        int: ATS score between 0-100
    """
    if not resume_text or len(resume_text) < 10:
        logger.warning("Resume text too short for ATS scoring")
        return 0
    
    total_score = 0
    keywords_found = 0
    
    for keyword, weight in ATS_KEYWORDS.items():
        # Count keyword occurrences
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = len(re.findall(pattern, resume_text, re.IGNORECASE))
        
        if matches > 0:
            keywords_found += 1
            # Award weight per occurrence, but with diminishing returns
            score_contribution = min(weight * matches, weight * 3)
            total_score += score_contribution
    
    # Bonus for resume length (250-2500 words is ideal)
    word_count = len(resume_text.split())
    if 250 <= word_count <= 2500:
        total_score += 10
    elif word_count > 2500:
        total_score += 5  # Slight bonus for content, but not ideal length
    
    # Bonus for keyword variety
    if keywords_found >= 10:
        total_score += 15
    elif keywords_found >= 5:
        total_score += 10
    
    # Normalize score to 100
    normalized_score = min(int(total_score / 5), 100)  # Adjusted scaling factor
    
    logger.info(f"Calculated ATS score: {normalized_score}/100 (keywords found: {keywords_found})")
    return normalized_score


def match_jobs(resume_text):
    """
    Match resume with job descriptions using TF-IDF and cosine similarity
    
    Args:
        resume_text (str): Cleaned resume text
        
    Returns:
        list: List of job matches sorted by match score (highest first)
    """
    if not resume_text or len(resume_text) < 20:
        logger.warning("Resume text insufficient for job matching")
        return []
    
    try:
        # Prepare documents: resume first, then job descriptions
        documents = [resume_text] + list(JOB_DESCRIPTIONS.values())
        
        # TF-IDF vectorization with reasonable parameters
        vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            min_df=1,
            max_df=0.8
        )
        vectors = vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity between resume and job descriptions
        similarity_scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
        
        results = []
        for idx, (job_title, _) in enumerate(JOB_DESCRIPTIONS.items()):
            match_percentage = round(float(similarity_scores[idx]) * 100, 2)
            results.append({
                "role": job_title,
                "match_score": match_percentage
            })
        
        # Sort by match score (highest first)
        results = sorted(results, key=lambda x: x["match_score"], reverse=True)
        
        logger.info(f"Job matching completed: {len(results)} roles matched")
        return results
        
    except Exception as e:
        logger.error(f"Job matching error: {e}")
        return []


def cleanup_old_files(max_age_hours=24):
    """
    Clean up old uploaded files to prevent disk space issues
    
    Args:
        max_age_hours (int): Maximum age of files to keep in hours
    """
    try:
        if not os.path.exists(UPLOAD_FOLDER):
            return
        
        current_time = datetime.now()
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            if os.path.isfile(file_path):
                file_age = (current_time - datetime.fromtimestamp(
                    os.path.getctime(file_path)
                )).total_seconds() / 3600
                
                if file_age > max_age_hours:
                    try:
                        os.remove(file_path)
                        logger.info(f"Cleaned up old file: {filename}")
                    except Exception as e:
                        logger.warning(f"Could not delete file {filename}: {e}")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")


# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def home():
    """Home page route"""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():
    """
    Handle resume upload and analysis
    
    Returns:
        Rendered results template or redirect to home
    """
    try:
        # Validate file presence
        if "resume" not in request.files:
            flash("No file selected. Please upload a resume.", "error")
            logger.warning("Upload attempt with no file")
            return redirect(url_for("home"))
        
        file = request.files["resume"]
        
        if file.filename == "":
            flash("Please select a file to upload.", "error")
            logger.warning("Upload attempt with empty filename")
            return redirect(url_for("home"))
        
        # Validate file type
        if not allowed_file(file.filename):
            flash("Invalid file type. Only PDF files are allowed.", "error")
            logger.warning(f"Upload attempt with invalid file type: {file.filename}")
            return redirect(url_for("home"))
        
        # Validate file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size == 0:
            flash("File is empty. Please upload a valid resume.", "error")
            logger.warning("Upload attempt with empty file")
            return redirect(url_for("home"))
        
        if file_size > MAX_FILE_SIZE:
            flash(f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024):.1f}MB.", "error")
            logger.warning(f"Upload attempt with oversized file: {file_size} bytes")
            return redirect(url_for("home"))
        
        # Create upload folder if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save file with sanitized filename
        filename = validate_filename(file.filename)
        # Add timestamp to prevent filename collisions
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        file.save(file_path)
        logger.info(f"File uploaded successfully: {filename}")
        
        # Extract and process resume
        try:
            resume_text = extract_text_from_pdf(file_path)
            resume_text = clean_text(resume_text)
            
            if not resume_text:
                flash("Could not extract text from the PDF. Please ensure it's a valid PDF.", "error")
                os.remove(file_path)  # Clean up failed file
                return redirect(url_for("home"))
            
            # Perform analysis
            skills = extract_skills(resume_text)
            ats_score = calculate_ats_score(resume_text)
            job_matches = match_jobs(resume_text)
            
            # Clean up the uploaded file after processing
            try:
                os.remove(file_path)
            except Exception as e:
                logger.warning(f"Could not delete processed file: {e}")
            
            logger.info(f"Resume analysis completed: {len(skills)} skills found, ATS score: {ats_score}")
            
            return render_template(
                "results.html",
                skills=skills,
                ats_score=ats_score,
                job_matches=job_matches,
                filename=filename
            )
            
        except (ValueError, FileNotFoundError) as e:
            flash(f"Error processing file: {str(e)}", "error")
            logger.error(f"Resume processing error: {e}")
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for("home"))
        
    except Exception as e:
        flash("An unexpected error occurred. Please try again.", "error")
        logger.error(f"Unexpected upload error: {e}", exc_info=True)
        return redirect(url_for("home"))


@app.route("/about")
def about():
    """About page route"""
    return render_template("about.html")


@app.route("/stats")
def stats():
    """Statistics page route (optional)"""
    stats_data = {
        "total_job_descriptions": len(JOB_DESCRIPTIONS),
        "total_skills_in_db": len(SKILLS_DB),
        "max_file_size_mb": MAX_FILE_SIZE / (1024 * 1024),
        "supported_extensions": ", ".join(ALLOWED_EXTENSIONS)
    }
    return render_template("stats.html", stats=stats_data)


# ----------------------------
# ERROR HANDLERS
# ----------------------------

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors"""
    flash("File is too large. Maximum size is 5MB.", "error")
    return redirect(url_for("home")), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template("error.html", message="Page not found."), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return render_template("error.html", message="An internal error occurred."), 500


# ----------------------------
# MAIN
# ----------------------------

if __name__ == "__main__":
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Clean up old files on startup
    cleanup_old_files(max_age_hours=24)
    
    logger.info("Starting Resume Analyzer Application")
    
    # Run app
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
