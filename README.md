AI Resume Analyzer 📝

AI Resume Analyzer is a full-stack, AI-powered web application that helps job seekers evaluate and improve their resumes by comparing them against specific job descriptions.
It simulates how Applicant Tracking Systems (ATS) and recruiters analyze resumes, providing structured scores, insights, and actionable feedback.

The project uses modern NLP models and a clean Flask + React (Vite) architecture for real-world scalability.

🚀 Key Features
📄 Resume Text Extraction

Upload resumes in PDF format

Automatically extracts and preprocesses resume text

🧾 Job Description Matching

Compare a resume against one or multiple job descriptions

Tailored analysis for each role

📊 ATS Similarity Scoring

Uses Sentence Transformers (all-mpnet-base-v2)

Computes semantic similarity between resume and job description

Reflects ATS-style keyword & context matching

🤖 AI-Powered Resume Evaluation

Powered by Groq LLM (LLaMA-based model)

Evaluates skills, experience, relevance, and alignment

Provides section-wise scoring and explanations

🧠 Actionable Feedback

Highlights strengths and gaps

Suggests improvements to increase shortlisting chances

📥 Downloadable PDF Report

Generate and download a detailed resume analysis report

Useful for tracking improvements over time

🛠 Tech Stack
Backend

Flask

Sentence Transformers

Groq LLM API

NumPy, Pandas, Scikit-learn

PDF Processing & Report Generation

Frontend

React

Vite

Modern UI with API-based integration

⚙️ Installation & Setup (Local)
✅ Prerequisites

Make sure you have:

Python 3.11

Node.js (LTS)

Git

🎯 Why Use This Tool?

ATS Optimization – Understand how automated systems read your resume

AI-Driven Feedback – Get structured insights without hiring a consultant

Role-Specific Analysis – Customize your resume per job description

End-to-End Workflow – Upload → Analyze → Improve → Download report

This project is ideal for:

Job seekers

Career coaches

HR-Tech research & academic projects

Developers exploring AI-driven document analysis

🔧 Customization Options

Change the embedding model (all-mpnet-base-v2)

Modify the LLM prompt for different evaluation styles

Replace Groq API with another LLM provider if required

Customize UI labels, scores, and report formats
