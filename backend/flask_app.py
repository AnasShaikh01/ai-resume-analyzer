import os
from typing import List

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# -------------------- Internal Imports --------------------

from resume_analyzer.reporting import generate_pdf_report
from resume_analyzer.analysis import analyze_resume_against_jd
from resume_analyzer.extraction import check_ats_compliance, load_skills
from resume_analyzer.processing import extract_text_from_file, preprocess
from resume_analyzer.utils import load_bert_model

# -------------------- App Initialization --------------------

app = Flask(__name__)

# -------------------- CORS Configuration --------------------

origins = [
    "http://localhost",
    "http://localhost:3000",   # React
    "http://localhost:5173",   # Vite
]

CORS(app, origins=origins, supports_credentials=True)

# -------------------- Environment & Config --------------------

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("⚠️ WARNING: GROQ_API_KEY is not set in environment variables")

# -------------------- Load ML Model ONCE (IMPORTANT) --------------------

print("🔹 Loading Sentence Transformer model (once at startup)...")
bert_model = load_bert_model()
print("✅ Sentence Transformer model loaded successfully")

# -------------------- API Endpoints --------------------

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "AI Resume Analyzer API is running."
    })


@app.route("/analyze-resume/", methods=["POST"])
def analyze_resume_endpoint():
    if not GROQ_API_KEY:
        return jsonify({
            "error": "GROQ_API_KEY is not configured on the server."
        }), 500

    if "resume_file" not in request.files:
        return jsonify({
            "error": "No resume file provided."
        }), 400

    resume_file = request.files["resume_file"]
    job_descriptions = request.form.getlist("job_descriptions")

    # Read file
    file_bytes = resume_file.read()
    file_ext = os.path.splitext(resume_file.filename)[-1].lower()

    # Resume processing
    raw_resume = extract_text_from_file(file_bytes, resume_file.filename)
    resume_text = preprocess(raw_resume)

    # ATS & skills
    ats_compliance = check_ats_compliance(file_bytes, file_ext)
    all_skills = load_skills("skills.csv")

    analysis_results = []

    for jd in job_descriptions:
        if jd and jd.strip():
            result = analyze_resume_against_jd(
                bert_model,
                resume_text,
                jd,
                all_skills,
                GROQ_API_KEY
            )
            result["ats_compliance"] = ats_compliance
            analysis_results.append(result)

    return jsonify({"results": analysis_results})


@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.json

    if not data or "result" not in data:
        return jsonify({
            "error": "No analysis data provided"
        }), 400

    result = data["result"]

    # Generate PDF (JD index = 0 for now)
    pdf_file = generate_pdf_report(0, result)

    return send_file(
        pdf_file,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="AI_Resume_Analysis_Report.pdf"
    )


# -------------------- App Runner --------------------

if __name__ == "__main__":
    """
    IMPORTANT:
    - debug=False prevents Flask auto-reloader
    - This ensures ML model is NOT reloaded repeatedly
    """
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
        use_reloader=False
    )
