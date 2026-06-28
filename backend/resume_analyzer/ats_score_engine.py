#ats_score_engine.py
import re
import numpy as np
import spacy
from sklearn.metrics.pairwise import cosine_similarity

class ATSScoreEngine:
    """
    Responsible ONLY for ATS-related scoring.

    Responsibilities
    ----------------
    ✓ Semantic Similarity
    ✓ Requirements Score
    ✓ Keyword Score
    ✓ Overall ATS Score

    Future Extensions
    -----------------
    - Context-aware scoring
    - Section weighting
    - Skill importance weighting
    """

    def __init__(self, model):
        self.model = model
        self.nlp = spacy.load("en_core_web_sm")
        self.section_weights = {
            "experience": 1.4,
            "projects": 1.3,
            "skills": 1.0,
            "summary": 0.8,
            "certifications": 0.8,
            "achievements": 0.7,
            "education": 0.5
        }

    # --------------------------------------------------
    # Semantic Similarity
    # --------------------------------------------------

    def semantic_similarity(
        self,
        resume_text,
        jd_text
    ):
        if not resume_text or not jd_text:
            return 0.0

        resume_embedding = self.model.encode([resume_text])
        jd_embedding = self.model.encode([jd_text])
        similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]

        return float(np.clip(similarity, 0.0, 1.0))

    # --------------------------------------------------
    # Requirements Score
    # --------------------------------------------------

    def requirements_score(
        self,
        matched_skills,
        jd_skills
    ):

        if not jd_skills:
            return 0

        return int((len(matched_skills) / len(jd_skills))* 100)

    # --------------------------------------------------
    # Keyword Score
    # --------------------------------------------------

    def keyword_score(
        self,
        resume_skills,
        jd_skills
    ):

        if not jd_skills:
            return 0

        matches = len(
            set(jd_skills).intersection(set(resume_skills))
        )

        return int((matches / len(jd_skills)) * 100)
        
    def context_score(
        self,
        matched_skills,
        resume_sections
    ):
        """
        Scores skills based on:
        1. Section importance
        2. Whether the skill is used in an action context
        (detected via SpaCy dependency parsing)
        """

        if not matched_skills:
            return 0

        total_score = 0.0
        max_weight = max(self.section_weights.values())
        max_score = len(matched_skills) * (max_weight + 0.5)
        
        for skill in matched_skills:
            best_score = 0.0
            for section, text in resume_sections.items():
                if not text.strip():
                    continue
                if skill.lower() not in text.lower():
                    continue
                section_weight = self.section_weights.get(section, 1.0)
                doc = self.nlp(text)
                context_bonus = 0.0
                
                for sent in doc.sents:
                    if skill.lower() not in sent.text.lower():
                        continue

                    for token in sent:
                        if skill.lower() not in token.text.lower():
                            continue
                        head = token.head
                        
                        if head.pos_ == "VERB":
                            context_bonus = 0.5
                            break

                        if any(child.pos_ == "VERB" for child in token.children):
                            context_bonus = 0.5
                            break

                    if context_bonus:
                        break

                best_score = max(best_score, section_weight + context_bonus)
            total_score += best_score

        return int((total_score / max_score) * 100)

    # --------------------------------------------------
    # Overall Score
    # --------------------------------------------------

    def overall_score(
        self,
        semantic_similarity,
        requirements_score,
        keyword_score,
        context_score
    ):

        semantic_score = int(round(semantic_similarity * 100))
        overall = int(
            0.40 * semantic_score +
            0.25 * requirements_score +
            0.15 * keyword_score +
            0.20 * context_score
        )
        if overall > 0:
            overall = max(overall, 50)
        return overall

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def calculate(
        self,
        resume_text,
        jd_text,
        resume_skills,
        jd_skills,
        matched_skills,
        resume_sections
    ):

        semantic = self.semantic_similarity(
            resume_text,
            jd_text
        )
        requirements = self.requirements_score(
            matched_skills,
            jd_skills
        )
        keywords = self.keyword_score(
            matched_skills,
            jd_skills
        )
        context = self.context_score(
            matched_skills,
            resume_sections
        )
        overall = self.overall_score(
            semantic,
            requirements,
            keywords,
            context
        )
        print("\n===== ATS SCORE BREAKDOWN =====")
        print(f"Semantic Similarity : {semantic:.3f}")
        print(f"Requirements Score  : {requirements}")
        print(f"Keyword Score       : {keywords}")
        print(f"Context Score       : {context}")
        print(f"Overall Score       : {overall}")

        return {
            "ats_score": semantic,
            "requirements_score": requirements,
            "keywords_score": keywords,
            "context_score": context,
            "overall_score": overall
        }