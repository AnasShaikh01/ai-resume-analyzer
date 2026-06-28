import re
import spacy


class ResumeSectionParser:

    def __init__(self):
        self.nlp = spacy.load(
            "en_core_web_sm"
        )

        self.section_patterns = {

            "summary": {
                "summary",
                "professional summary",
                "profile",
                "objective",
                "career objective"
            },

            "skills": {
                "skills",
                "technical skills",
                "core competencies",
                "technical expertise"
            },

            "experience": {
                "experience",
                "work experience",
                "professional experience",
                "employment history"
            },

            "projects": {
                "projects",
                "academic projects",
                "personal projects"
            },

            "education": {
                "education",
                "academic background",
                "qualifications"
            },

            "certifications": {
                "certifications",
                "certificates",
                "licenses"
            },

            "achievements": {
                "achievements",
                "awards",
                "honors"
            }
        }

    def _normalize_text(self, text):
        return re.sub(
            r"[^a-zA-Z ]",
            "",
            text
        ).strip().lower()

    def _is_heading(self, line):
        line = line.strip()
        if not line:
            return False

        words = line.split()

        if len(words) > 5:
            return False

        if line.isupper():
            return True

        if line.istitle():
            return True

        return False

    def _detect_section(self, line):
        normalized = self._normalize_text(
            line
        )
        for section, headings in (
            self.section_patterns.items()
        ):
            if normalized in headings:
                return section
        return None

    def parse(self, resume_text):

        print("\n===== PARSER CALLED =====")
        sections = {
            "summary": "",
            "skills": "",
            "experience": "",
            "projects": "",
            "education": "",
            "certifications": "",
            "achievements": ""
        }

        current_section = None

        lines = [
            line.strip()
            for line in resume_text.splitlines()
            if line.strip()
        ]
        print("\n===== FIRST 30 LINES =====")

        for line in lines[:30]:
            print(repr(line))

        for line in lines:
            detected_section = None
            normalized_line = self._normalize_text(
                line
            )

            for section, headings in self.section_patterns.items():
                for heading in headings:
                    if normalized_line.startswith(heading):
                        detected_section = section
                        break

                if detected_section:
                    break

            if detected_section:
                current_section = detected_section
                continue
            
            if current_section:
                sections[current_section] += (line + "\n")
                        
        print("\n===== PARSED SECTIONS =====")

        for k, v in sections.items():

            print(
                f"{k}: {len(v)} chars"
            )
        return sections