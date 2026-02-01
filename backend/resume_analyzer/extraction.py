import io
import re
import os
import docx
import fitz  # PyMuPDF
import pandas as pd

def load_skills(csv_path="skills.csv"):
    """
    Loads skills from CSV.
    - If CSV has one column → returns list of skills.
    - If CSV has two columns (skill, alias) → returns dict {canonical: [aliases]}.
    """
    # Construct an absolute path to skills.csv relative to this file's location
    # This ensures it's found regardless of where the app is run from.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_csv_path = os.path.join(current_dir, '..', '..', csv_path)
    try:
        df = pd.read_csv(absolute_csv_path, header=None)
    except FileNotFoundError:
        return [] # Return empty list if skills.csv is not found

    if df.shape[1] == 1:
        # Single-column → simple list
        return [skill.lower().strip() for skill in df[0].dropna().tolist()]
    elif df.shape[1] >= 2:
        # Two-column → dict with aliases
        skills_dict = {}
        for _, row in df.iterrows():
            canonical = str(row[0]).strip().lower()
            alias = str(row[1]).strip().lower()
            if canonical:
                if canonical not in skills_dict:
                    skills_dict[canonical] = []
                if alias and alias not in skills_dict[canonical]:
                    skills_dict[canonical].append(alias)
        return skills_dict
    else:
        return []

def extract_skills(text, skills_source):
    """
    Extracts skills from text.
    - Works with list (simple skills).
    - Works with dict (canonical + aliases).
    """
    text = text.lower()
    found = set()

    if isinstance(skills_source, list):
        for skill in skills_source:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text):
                found.add(skill)

    elif isinstance(skills_source, dict):
        for canonical, aliases in skills_source.items():
            all_terms = [canonical] + aliases
            for term in all_terms:
                pattern = r'\b' + re.escape(term) + r'\b'
                if re.search(pattern, text):
                    found.add(canonical)  # always return canonical
                    break

    return list(found)


def _normalize_font_name(name: str) -> str:
    """Clean up PDF font names like 'AAAAAA+Calibri-Bold' -> 'Calibri'."""
    if not name:
        return ""
    name = name.split("+")[-1]  # remove prefix
    name = re.sub(r"[- ]?(Bold|Italic|Oblique|Regular)$", "", name, flags=re.IGNORECASE)
    return name.strip()

def _detect_multi_column(page) -> bool:
    """Detect if a PDF page is multi-column using clustering of x positions."""
    blocks = page.get_text("blocks")
    if not blocks or len(blocks) < 10: return False

    x_positions = [b[0] for b in blocks]
    clustered = [round(x / 20) * 20 for x in x_positions]
    cluster_counts = {}
    for c in clustered:
        cluster_counts[c] = cluster_counts.get(c, 0) + 1

    sorted_clusters = sorted(cluster_counts.items(), key=lambda x: -x[1])

    if len(sorted_clusters) >= 2:
        (x1, count1), (x2, count2) = sorted_clusters[0], sorted_clusters[1]
        distance = abs(x1 - x2)
        if distance > page.rect.width * 0.35 and count1 > 5 and count2 > 5:
            return True
    return False

def check_ats_compliance(file_bytes, file_type: str):
    """Check resume file for ATS-unfriendly formatting."""
    results = {
        "multi_column": False,
        "non_standard_fonts": False,
        "images": False,
        "tables": False
    }
    bad_fonts = {"Comic Sans", "Papyrus", "Brush Script", "Cursive", "Monotype Corsiva"}

    try:
        if file_type == "pdf":
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                # Images
                for img in page.get_images(full=True):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n >= 3 and pix.width > 100 and pix.height > 100:
                        results["images"] = True; break
                # Fonts
                for f in page.get_fonts():
                    font_name = _normalize_font_name(f[3])
                    if any(bad.lower() in font_name.lower() for bad in bad_fonts):
                        results["non_standard_fonts"] = True; break
                # Columns
                if _detect_multi_column(page):
                    results["multi_column"] = True
                if any(results.values()): break
            doc.close()

        elif file_type == "docx":
            doc = docx.Document(io.BytesIO(file_bytes))
            if len(doc.tables) > 0: results["tables"] = True
            if len(doc.inline_shapes) > 0: results["images"] = True
            if len(doc.sections) > 1 and doc.sections[0].start_type != 2:
                results["multi_column"] = True
            for para in doc.paragraphs:
                for run in para.runs:
                    if run.font.name and any(bad.lower() in run.font.name.lower() for bad in bad_fonts):
                        results["non_standard_fonts"] = True; break
                if results["non_standard_fonts"]: break

    except Exception as e:
        results["error"] = str(e)

    return results
