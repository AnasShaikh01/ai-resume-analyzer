import spacy
from spacy.matcher import PhraseMatcher
from spacy.util import filter_spans

class SkillExtractor:
    def __init__(self, skills_source):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self.skill_map = {}
        patterns = []

        # --------------------------------------------------
        # Skills List
        # --------------------------------------------------

        if isinstance(skills_source, list):
            for skill in skills_source:
                skill = skill.strip().lower()
                self.skill_map[skill] = skill
                patterns.append(self.nlp.make_doc(skill))

        # --------------------------------------------------
        # Skills Dictionary (Canonical + Aliases)
        # --------------------------------------------------

        elif isinstance(skills_source, dict):

            for canonical, aliases in skills_source.items():
                canonical = canonical.strip().lower()
                self.skill_map[canonical] = canonical
                patterns.append(self.nlp.make_doc(canonical))

                for alias in aliases:
                    alias = alias.strip().lower()
                    self.skill_map[alias] = canonical
                    patterns.append(self.nlp.make_doc(alias))

        self.matcher.add("SKILLS", patterns)

    # --------------------------------------------------
    # Skill Extraction
    # --------------------------------------------------

    def extract(self, text):

        doc = self.nlp(text)
        matches = filter_spans([doc[start:end] for _, start, end in self.matcher(doc)])
        extracted = set()

        for span in matches:
            skill_text = span.text.lower()
            canonical = self.skill_map.get(
                skill_text,
                skill_text
            )
            extracted.add(canonical)

        return sorted(extracted)