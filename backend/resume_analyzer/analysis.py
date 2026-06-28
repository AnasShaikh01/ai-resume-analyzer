from .ats_score_engine import ATSScoreEngine
from .llm import (
    get_report_structured,
    generate_learning_suggestions
)
from .processing import (
    preprocess_resume,
    preprocess_jd
)
from .extraction import (
    extract_skills,
    parse_resume_sections
)
from .semantic_matcher import semantic_skill_matching


def analyze_resume_against_jd(
    model,
    resume: str,
    jd_text: str,
    all_skills: list,
    api_key: str
):
    """
    Analyze resume against a job description.
    """
    # --------------------------------------------------
    # Resume Processing
    # --------------------------------------------------

    resume_sections = parse_resume_sections(
        resume
    )

    resume_clean = preprocess_resume(
        resume
    )

    for section, content in resume_sections.items():

        if content.strip():

            print(
                f"{section.upper()} "
                f"({len(content)} chars)"
            )

    # --------------------------------------------------
    # JD Processing
    # --------------------------------------------------

    jd_clean = preprocess_jd(
        jd_text
    )

    jd_skills = (
        extract_skills(
            jd_clean,
            all_skills
        )
        if all_skills is not None
        else []
    )

    skills_found = (
        extract_skills(
            resume_clean,
            all_skills
        )
        if all_skills is not None
        else []
    )

    # --------------------------------------------------
    # Section Skills
    # --------------------------------------------------

    section_skills = {}

    if all_skills is not None:

        for (
            section_name,
            section_text
        ) in resume_sections.items():

            section_skills[
                section_name
            ] = extract_skills(
                section_text,
                all_skills
            )

    # --------------------------------------------------
    # Skill Location Mapping
    # --------------------------------------------------

    skill_locations = {}

    for (
        section,
        skills
    ) in section_skills.items():

        for skill in skills:

            skill_locations.setdefault(
                skill,
                []
            ).append(section)

    print("\n===== SKILL LOCATIONS =====")

    for (
        skill,
        sections
    ) in skill_locations.items():

        print(
            f"{skill} -> {sections}"
        )

    print("\n===== SECTION SKILLS =====")

    for (
        section,
        skills
    ) in section_skills.items():

        print(
            f"{section}: {skills}"
        )

    print("\n===== JD SKILLS =====")
    print(jd_skills)

    print("\n===== RESUME SKILLS =====")
    print(skills_found)

    # --------------------------------------------------
    # Skill Matching
    # --------------------------------------------------

    skill_results = semantic_skill_matching(
        model,
        jd_skills,
        skills_found
    )

    matched_skills = skill_results["matched_skills"]
    missing_skills = skill_results["missing_skills"]
    additional_skills = skill_results["additional_skills"]

    # --------------------------------------------------
    # Learning Suggestions
    # --------------------------------------------------

    learning_suggestions = {}

    if missing_skills:

        learning_suggestions = (
            generate_learning_suggestions(
                missing_skills,
                api_key
            )
        )

    # --------------------------------------------------
    # AI Report
    # --------------------------------------------------

    ai_report_text = get_report_structured(
        resume,
        jd_text,
        api_key
    )

    ats_engine = ATSScoreEngine(model)

    scores = ats_engine.calculate(
        resume_text=resume,
        jd_text=jd_text,
        resume_skills=skills_found,
        jd_skills=jd_skills,
        matched_skills=matched_skills,
        resume_sections=resume_sections
    )

    # --------------------------------------------------
    # Return
    # --------------------------------------------------

    return {
        "jd_text": jd_text,
        "resume_sections": resume_sections,
        "section_skills": section_skills,
        "ats_score": scores["ats_score"],
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "learning_suggestions": learning_suggestions,
        "ai_raw": ai_report_text,
        "requirements_score": scores["requirements_score"],
        "keywords_score": scores["keywords_score"],
        "context_score": scores["context_score"],
        "overall_score": scores["overall_score"],
    }