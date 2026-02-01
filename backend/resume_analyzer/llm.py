import datetime
import re
from groq import Groq

def extract_candidate_name(resume_text: str) -> str:
    """Extract a reasonable candidate name from top lines of resume text."""
    if not resume_text or not resume_text.strip():
        return "the candidate"

    stop_words = {
        "software", "solutions", "technologies", "developer", "engineer", "consultant",
        "founder", "director", "manager", "architect", "inc", "ltd", "llc", "pvt",
        "company", "enterprise", "enterprises", "services", "systems", "consulting",
        "resume", "cv", "curriculum", "vitae", "student", "full", "stack"
    }

    lines = [ln.strip() for ln in resume_text.splitlines() if ln.strip()]
    if not lines:
        return "the candidate"

    # Look for a likely name in the first 2 non-empty lines
    first_line = lines[0]
    if len(lines) > 1 and len(lines[0].split()) < 2:
        first_line = lines[1]

    # Remove emails, phones, separators
    first_line = re.sub(r'\b\S+@\S+\b', ' ', first_line)
    first_line = re.sub(r'\+?\d[\d\-\s\(\)]{6,}\d', ' ', first_line)
    first_line = re.sub(r'[|,/\\\-–—]', ' ', first_line)
    first_line = re.sub(r'\s{2,}', ' ', first_line).strip()

    tokens = first_line.split()
    cleaned = [t for t in tokens if t.lower() not in stop_words]

    if not cleaned:
        return "the candidate"

    return " ".join(cleaned[:3]).title()

def get_report_structured(resume: str, job_desc: str, groq_api_key: str):
    """Generate a clean, plain-text structured report (no markdown asterisks)."""

    # ------------------ Setup Groq client ------------------
    try:
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        print(f"🚨 Failed to initialize Groq client: {e}")
        return None

    candidate_name = extract_candidate_name(resume)

    # ------------------ Extract job info ------------------
    first_line = job_desc.strip().splitlines()[0] if job_desc.strip() else ""
    job_title, company = "the given role", "the company"
    if " at " in first_line:
        parts = first_line.split(" at ", 1)
        job_title = parts[0].strip() or job_title
        company = parts[1].strip() or company
    elif first_line:
        job_title = first_line.strip()

    # ------------------ Prompt ------------------
    system_msg = f"""
You are an expert resume analyst. 
Generate a professional, well-structured plain-text report — do not use markdown symbols, asterisks, or bullet points with stars.

Analyze {candidate_name}'s resume for the position of {job_title} at {company}.

Follow exactly this format:

Analyzing {candidate_name}'s resume in the context of the job description for
a {job_title} at {company} reveals several strengths and areas for improvement.

1. Strengths:
- Highlight relevant education (degree, specialization, GPA if available)
- List technical skills that match the JD
- Cover projects that demonstrate practical expertise
- Mention work experience or certifications that align with the JD

2. Areas for Improvement:
- Tailor resume to the JD (missing technologies or misalignment)
- Professional summary (if missing or too generic)
- Work experience (add achievements, quantify results)
- Projects (show outcomes, add GitHub links)
- Soft skills (if weak, suggest examples)
- Formatting and clarity
- Redundant or outdated information to remove

3. In-Depth Section Analysis:
Education: strengths and weaknesses
Skills: coverage and missing JD-specific skills
Projects: depth, outcomes, missing links
Work Experience: responsibilities, achievements, or gaps
Certifications: presence and relevance

4. Soft Skills Coverage:
Teamwork - Present / Absent / Implied (+ recommendation)
Leadership - Present / Absent / Implied
Communication - Present / Absent / Implied
Recommendation: how to integrate these naturally into resume sections

5. Suggested Resume Structure:
Header: name, contact info, LinkedIn
Professional Summary: tailored to JD and key fit
Education: relevance and coursework
Technical Skills: grouped logically
Projects: emphasize JD-relevant ones
Work Experience: quantified achievements
Certifications: relevant ones only
Soft Skills: include examples

Formatting rules:
- No special markdown symbols (like *, **, or #)
- Use plain dashes for lists (-)
- Keep exactly one blank line between sections
- Keep tone professional and actionable
"""

    user_msg = (
        "Resume:\n" + resume.strip() + "\n\n" +
        "Job Description:\n" + job_desc.strip() + "\n\n" +
        "Follow the exact structure and clean formatting above. "
        "Do not use markdown or asterisks in your output."
    )

    # ------------------ API Call ------------------
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
        )

        if not response.choices or not response.choices[0].message.content:
            print("🚨 Groq returned an empty or invalid response.")
            return None

        raw_text = response.choices[0].message.content.strip()

        # --- Simplified Post-processing to complement the prompt ---
        # The prompt is strict, so we only need to handle minor inconsistencies.
        lines = raw_text.split('\n')
        processed_lines = []
        for line in lines:
            # 1. Normalize list markers to a consistent "- "
            clean_line = re.sub(r"^\s*[\*\-]\s+", "- ", line)

            # 2. Capitalize the first letter of list items for a professional look.
            if clean_line.startswith('- ') and len(clean_line) > 2:
                clean_line = '- ' + clean_line[2].upper() + clean_line[3:]
            processed_lines.append(clean_line)
        
        # 3. Join lines and normalize blank lines to ensure consistent paragraph spacing.
        cleaned_text = '\n'.join(processed_lines)
        cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text).strip()

        return cleaned_text

    except Exception as e:
        print(f"🚨 Groq API call failed at {datetime.datetime.now()}: {e}")
        return None

def generate_learning_suggestions(missing_skills, api_key):
    """
    Returns learning resources for missing skills.
    Falls back to static resources if LLM fails.
    """

    # --- STATIC FALLBACK RESOURCES ---
    fallback_resources = {
        "java": [
            "Oracle Java Documentation",
            "Java Full Course – freeCodeCamp (YouTube)",
            "GeeksforGeeks Java Programming"
        ],
        "c": [
            "C Programming Tutorial – GeeksforGeeks",
            "C Full Course – freeCodeCamp (YouTube)",
            "Learn C – Tutorialspoint"
        ],
        "python": [
            "Official Python Documentation",
            "Python Full Course – freeCodeCamp (YouTube)",
            "Real Python Tutorials"
        ],
        "javascript": [
            "MDN JavaScript Guide",
            "JavaScript Full Course – freeCodeCamp (YouTube)",
            "JavaScript.info"
        ],
    }

    suggestions = {}

    try:
        # 🔥 If you later want LLM, keep it here
        # For now, we GUARANTEE output using fallback

        for skill in missing_skills:
            key = skill.lower()
            if key in fallback_resources:
                suggestions[key] = fallback_resources[key]
            else:
                suggestions[key] = [
                    f"Search '{skill}' tutorials on YouTube",
                    f"Read official {skill} documentation",
                    f"Practice {skill} on coding platforms"
                ]

    except Exception as e:
        print("Learning suggestion generation failed:", e)

        # Absolute fallback (never empty)
        for skill in missing_skills:
            suggestions[skill.lower()] = [
                f"Learn {skill} basics from online tutorials",
                f"Read documentation for {skill}"
            ]

    return suggestions

