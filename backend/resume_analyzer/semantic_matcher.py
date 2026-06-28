from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def semantic_skill_matching(
    model,
    jd_skills,
    resume_skills,
    threshold=0.85
):

    matched_skills = []
    matched_resume_skills = set()
    used_resume_indices = set()
    missing_skills = []

    if not jd_skills:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "additional_skills": []
        }

    if not resume_skills:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "additional_skills": []
        }
            
    print("\n===== SEMANTIC MATCHING =====")

    jd_embeddings = model.encode(jd_skills)
    resume_embeddings = model.encode(resume_skills)
    
    similarity_matrix = cosine_similarity(
        jd_embeddings,
        resume_embeddings
    )

    pairs = []

    for jd_idx, jd_skill in enumerate(jd_skills):
        adaptive_threshold = get_threshold(jd_skill)

        for resume_idx, resume_skill in enumerate(resume_skills):
            score = similarity_matrix[jd_idx][resume_idx]

            if score >= adaptive_threshold:
                pairs.append(
                    (score, jd_idx, resume_idx)
                )
    pairs.sort(reverse=True)

    used_jd = set()

    for score, jd_idx, resume_idx in pairs:
        if jd_idx in used_jd:
            continue

        if resume_idx in used_resume_indices:
            continue

        matched_skills.append(jd_skills[jd_idx])
        matched_resume_skills.add(resume_skills[resume_idx])

        used_jd.add(jd_idx)
        used_resume_indices.add(resume_idx)

        print(
            f"{jd_skills[jd_idx]} -> "
            f"{resume_skills[resume_idx]} = {score:.3f}"
        )
        
    for idx, skill in enumerate(jd_skills):
        if idx not in used_jd:
            missing_skills.append(skill)

    additional_skills = [
        skill
        for idx, skill in enumerate(resume_skills)
        if idx not in used_resume_indices
    ]

    print("\nSkill Matching Complete")

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills
    }

def get_threshold(skill):

    words = len(skill.split())

    if words >= 3:
        return 0.80

    elif words == 2:
        return 0.83

    return 0.85