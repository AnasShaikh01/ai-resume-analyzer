import re
from .utils import calculate_similarity_bert
from .llm import get_report_structured, generate_learning_suggestions
from .processing import preprocess
from .extraction import extract_skills


def analyze_resume_against_jd(model, resume: str, jd_text: str, all_skills: list, api_key: str):
    """Analyze resume vs a job description and return a result dict."""
    # Semantic similarity (0..1)
    ats_score = calculate_similarity_bert(model, resume, jd_text)

    # Clean JD for skill extraction
    jd_clean = preprocess(jd_text)
    jd_skills = extract_skills(jd_clean, all_skills) if all_skills is not None else []
    skills_found = extract_skills(resume, all_skills) if all_skills is not None else []

    matching_skills = [s for s in jd_skills if s in skills_found]
    missing_skills = [s for s in jd_skills if s not in skills_found]
    extra_skills = [s for s in skills_found if s not in jd_skills]

    # AI learning suggestions (best-effort)
    learning_suggestions = {}

    if missing_skills:
        learning_suggestions = generate_learning_suggestions(missing_skills, api_key)

    # AI feedback report (Groq)
    ai_report_text = get_report_structured(resume, jd_text, api_key)

    # Requirements score (safe division)
    requirements_score = int((len(matching_skills) / len(jd_skills)) * 100) if jd_skills else 0

    # Keywords score using regex word boundaries
    keyword_matches = 0
    for skill in jd_skills:
        try:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, resume, flags=re.IGNORECASE):
                keyword_matches += 1
        except re.error:
            # if skill contains regex-unfriendly chars, fall back to simple substring check
            if skill.lower() in resume.lower():
                keyword_matches += 1

    keywords_score = int((keyword_matches / len(jd_skills)) * 100) if jd_skills else 0

    # Hybrid overall score (weighted)
    semantic_score = int(round(ats_score * 100))

    overall_score = int(
        0.5 * semantic_score +   # 50% weight
        0.3 * requirements_score + # 30% weight
        0.2 * keywords_score     # 20% weight
    )

    # Normalization to avoid demotivating very low scores
    if overall_score > 0:
        overall_score = max(overall_score, 50)

    return {
        "jd_text": jd_text,
        "ats_score": ats_score,
        "jd_skills": jd_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "learning_suggestions": learning_suggestions,
        "ai_raw": ai_report_text,
        "requirements_score": requirements_score,
        "keywords_score": keywords_score,
        "overall_score": overall_score
    }
