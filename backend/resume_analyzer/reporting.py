import io
from fpdf import FPDF

class PDF(FPDF):
    """Custom PDF class to include a header and footer."""
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'AI Resume Analysis Report', 0, 0, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(240, 240, 240)  # Light grey background
        self.cell(0, 8, title, 0, 1, 'L', fill=True)
        self.ln(4)

    def chapter_body(self, body_text):
        self.set_font('Arial', '', 11)
        # Encode safely for FPDF, which uses latin-1
        safe_text = body_text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, safe_text)
        self.ln()

    def skill_list(self, title, skills):
        if not skills:
            return
        self.set_font('Arial', 'B', 11)
        self.cell(0, 7, f"{title} ({len(skills)}):")
        self.ln()
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, ', '.join(skills))
        self.ln(4)

    def ats_check_list(self, compliance_results):
        """Renders the ATS compliance check results."""
        self.set_font('Arial', '', 11)
        checks = {
            "multi_column": "Multi-column Layout",
            "non_standard_fonts": "Non-standard Fonts",
            "images": "Images or Graphics",
            "tables": "Tables"
        }
        for key, description in checks.items():
            issue_detected = compliance_results.get(key, False)
            status_text = "[ISSUE]" if issue_detected else "[OK]"
            self.cell(0, 7, f"{status_text} {description}: {'Detected' if issue_detected else 'Not Detected'}", ln=True)

def generate_pdf_report(jd_index: int, res: dict):
    """
    Generates a well-structured PDF report from the analysis results.

    Args:
        jd_index (int): The index of the job description (for labeling).
        res (dict): The dictionary containing the analysis results.

    Returns:
        io.BytesIO: An in-memory byte stream of the generated PDF.
    """
    pdf = PDF()
    pdf.add_page()
    
    # --- Title ---
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, f"Analysis for Job Description {jd_index+1}", ln=True, align="C")
    pdf.ln(5)

    # --- Top-level Scores ---
    pdf.chapter_title("Overall Summary")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, f"Overall Match Score: {res.get('overall_score', 0)}%", ln=True)
    pdf.cell(0, 7, f"Semantic Similarity (ATS Score): {res.get('ats_score', 0.0):.2%}", ln=True)
    pdf.ln(5)

    # --- Skill Analysis ---
    pdf.chapter_title("Skill Match Analysis")
    pdf.skill_list("Matching Skills", res.get('matching_skills', []))
    pdf.skill_list("Missing Skills", res.get('missing_skills', []))
    pdf.skill_list("Extra Skills (Not in JD)", res.get('extra_skills', []))
    pdf.ln(5)
    
    # --- ATS Compliance Analysis ---
    pdf.chapter_title("ATS Compliance Check")
    ats_results = res.get("ats_compliance", {})
    pdf.ats_check_list(ats_results)
    pdf.ln(5)

    # --- AI Detailed Report ---
    pdf.chapter_title("Detailed AI Analysis")
    ai_report = res.get("ai_raw", "No AI analysis available.")
    pdf.chapter_body(ai_report)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output
